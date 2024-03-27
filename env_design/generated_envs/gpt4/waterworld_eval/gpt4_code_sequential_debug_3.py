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
        self.green_circles_count = 0
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.green_circles_count += 1
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if not any(sprite.rect.topleft == (x, y) for sprite in self.circles):
                circle = Circle(color)
                circle.rect.topleft = (x, y)
                self.circles.add(circle)
                break

    def update_circles(self):
        self.circles.update()
        for circle in list(self.circles):
            if pygame.sprite.collide_rect(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                    self.green_circles_count -= 1
                else:
                    self.score -= 1
                self.circles.remove(circle)
                new_color = random.choice([GREEN, RED])
                self.spawn_circle(new_color)
                if new_color == GREEN:
                    self.green_circles_count += 1
                if self.green_circles_count == 0:
                    self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.green_circles_count = 5
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

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
        self.render_game()
        self.clock.tick(FPS)
        return not self.game_over

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.agent.draw(self.screen)
        font = pygame.font.Font(None, 36)
        score_text = f'Score: {self.score}'
        text_surface = font.render(score_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart')
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def move(self, pressed_keys):
        dx, dy = 0, 0
        if pressed_keys[pygame.K_UP]:
            dy = -GRID_SIZE
        if pressed_keys[pygame.K_DOWN]:
            dy = GRID_SIZE
        if pressed_keys[pygame.K_LEFT]:
            dx = -GRID_SIZE
        if pressed_keys[pygame.K_RIGHT]:
            dx = GRID_SIZE
        self.rect.move_ip(dx, dy)
        self.rect.clamp_ip(self.screen.get_rect())

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def move_smoothly(self):
        x_move = random.choice([-GRID_SIZE, 0, GRID_SIZE])
        y_move = random.choice([-GRID_SIZE, 0, GRID_SIZE])
        self.rect.x = (self.rect.x + x_move) % WIDTH
        self.rect.y = (self.rect.y + y_move) % HEIGHT

    def update(self):
        self.move_smoothly()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                game.agent.move(keys)
        game.run(None)
    pygame.quit()
