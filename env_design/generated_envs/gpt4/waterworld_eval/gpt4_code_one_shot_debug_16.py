import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60
CIRCLE_RADIUS = 10

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WaterWorld Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 25)

        self.agent = Agent()
        self.all_sprites = pygame.sprite.Group()
        self.circles = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        new_circle = Circle(color)
        while True:
            new_circle.rect.topleft = (random.randrange(GRID_WIDTH) * GRID_SIZE, random.randrange(GRID_HEIGHT) * GRID_SIZE)
            if pygame.sprite.spritecollideany(new_circle, self.circles) is None:
                break
        self.circles.add(new_circle)
        self.all_sprites.add(new_circle)

    def update_circles(self):
        for circle in list(self.circles):
            if self.agent.rect.colliderect(circle.rect):
                self.score += 1 if circle.color == GREEN else -1
                circle.kill()
                self.spawn_circle(random.choice([GREEN, RED]))
        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        self.agent.reset()
        self.circles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.agent)
        self.score = 0
        self.game_over = False
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()
        if not self.game_over and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        for circle in self.circles:
            circle.move_smoothly()
        self.all_sprites.draw(self.screen)
        score_text = self.font.render('Score: ' + str(self.score), True, BLACK)
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message("Game Over!")
        pygame.display.flip()

    def show_message(self, message, size=50):
        font = pygame.font.SysFont('Arial', size)
        message_surface = font.render(message, True, BLACK)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
        self.render_game()
        self.clock.tick(FPS)
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        if direction == pygame.K_UP:
            self.rect.y -= GRID_SIZE
        elif direction == pygame.K_DOWN:
            self.rect.y += GRID_SIZE
        elif direction == pygame.K_LEFT:
            self.rect.x -= GRID_SIZE
        elif direction == pygame.K_RIGHT:
            self.rect.x += GRID_SIZE
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def move_smoothly(self):
        dx, dy = random.choice([-2, -1, 0, 1, 2]), random.choice([-2, -1, 0, 1, 2])
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
