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
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.score = 0
        self.green_count = 0
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        count = GRID_WIDTH * GRID_HEIGHT // 40
        for _ in range(count // 2):
            self.spawn_circle(GREEN)
            self.green_count += 1
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle = Circle(color)
            new_circle.rect.topleft = (x, y)
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                break

    def update_circles(self):
        for circle in pygame.sprite.spritecollide(self.agent, self.circles, dokill=True):
            if circle.color == GREEN:
                self.score += 1
                self.green_count -= 1
            else:
                self.score -= 1
            new_color = GREEN if random.choice([True, False]) else RED
            self.spawn_circle(new_color)
            if new_color == GREEN:
                self.green_count += 1
        if self.green_count <= 0:
            self.game_over = True

    def reset_game(self):
        self.score = 0
        self.green_count = 0
        self.game_over = False
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))
        self.circles.draw(self.screen)
        self.agent.draw()
        if self.game_over:
            self.show_message("Game Over! Press 'R' to restart.")
        pygame.display.flip()

    def show_message(self, message, size=36):
        message_surface = self.font.render(message, True, BLUE)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def run(self):
        self.clock.tick(FPS)
        if not self.game_over:
            self.update_circles()
        self.render_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_events(event)


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        move_map = {
            pygame.K_UP: (0, -GRID_SIZE),
            pygame.K_DOWN: (0, GRID_SIZE),
            pygame.K_LEFT: (-GRID_SIZE, 0),
            pygame.K_RIGHT: (GRID_SIZE, 0)
        }
        if direction in move_map:
            self.rect.move_ip(move_map[direction])
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    def draw(self):
        self.screen.blit(self.image, self.rect)

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
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.vel = random.uniform(1, 3)  # Random velocity

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def update(self):
        self.move_smoothly()
        if random.randint(0, 10) == 0:  # Randomly change direction
            self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])

    def move_smoothly(self):
        self.rect.x += self.direction[0] * self.vel
        self.rect.y += self.direction[1] * self.vel
        # Keep the circle within the window bounds
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        running = game.run()
    pygame.quit()