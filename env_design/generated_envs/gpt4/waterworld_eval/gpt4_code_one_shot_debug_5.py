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
        self.agent = Agent()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()
        self.font = pygame.font.SysFont('arial', 24)

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        while True:
            new_circle = Circle(color)
            location = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            new_circle.rect.topleft = location
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                self.all_sprites.add(new_circle)
                break

    def update_circles(self):
        for circle in list(self.circles):
            if self.agent.rect.colliderect(circle.rect):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                self.circles.remove(circle)
                self.all_sprites.remove(circle)
                self.spawn_circle(random.choice([RED, GREEN]))

        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.agent.reset()
        self.all_sprites.empty()
        self.all_sprites.add(self.agent)
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.agent.move((0, -GRID_SIZE))
            elif event.key == pygame.K_DOWN:
                self.agent.move((0, GRID_SIZE))
            elif event.key == pygame.K_LEFT:
                self.agent.move((-GRID_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                self.agent.move((GRID_SIZE, 0))
            elif event.key == pygame.K_r and self.game_over:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        for circle in self.circles:
            self.screen.blit(circle.image, circle.rect)
        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', 48)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont('arial', size)
        message_surface = font.render(message, True, RED)
        message_rect = message_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        if not self.game_over:
            self.clock.tick(FPS)
            self.handle_events(event)
            self.update_circles()
            self.all_sprites.update()
            self.render_game()
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        self.rect.x += direction[0]
        self.rect.y += direction[1]
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()

    def reset(self):
        location = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                    random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.rect.topleft = location

    def update(self):
        direction = random.choice([(GRID_SIZE,0), (0,GRID_SIZE), (-GRID_SIZE,0), (0,-GRID_SIZE)])
        if pygame.Rect(0, 0, WIDTH, HEIGHT).contains(self.rect.move(direction)):
            self.rect.move_ip(direction)
        else:
            self.reset()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
