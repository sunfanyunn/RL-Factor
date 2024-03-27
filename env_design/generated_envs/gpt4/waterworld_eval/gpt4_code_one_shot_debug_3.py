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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WaterWorld Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 24)
        self.agent = Agent()
        self.agent_group = pygame.sprite.Group(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):  # Ten of each for a start
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            circle = Circle(color)
            circle.rect.topleft = pos
            if not pygame.sprite.spritecollide(circle, self.circles, False):
                self.circles.add(circle)
                break

    def update_circles(self):
        for circle in list(self.circles):
            circle.move_smoothly()
            if pygame.sprite.collide_rect(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(random.choice([GREEN, RED]))
        green_circles = sum(1 for circle in self.circles if circle.color == GREEN)
        if green_circles == 0:
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        score_text = self.font.render('Score: {}'.format(self.score), True, BLUE)
        self.screen.blit(score_text, (20, 20))

        if self.game_over:
            self.show_message("Game Over!")

        self.agent_group.draw(self.screen)
        self.circles.draw(self.screen)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont('Arial', size)
        text_surface = font.render(message, True, RED)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        if event:
            self.handle_events(event)
        if not self.game_over:
            self.agent.move_with_keys()
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

    def move_with_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= GRID_SIZE
        if keys[pygame.K_DOWN]:
            self.rect.y += GRID_SIZE
        if keys[pygame.K_LEFT]:
            self.rect.x -= GRID_SIZE
        if keys[pygame.K_RIGHT]:
            self.rect.x += GRID_SIZE
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def move_smoothly(self):
        self.rect.x += self.direction[0] * 2
        self.rect.y += self.direction[1] * 2
        self.rect.x %= WIDTH
        self.rect.y %= HEIGHT


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()

