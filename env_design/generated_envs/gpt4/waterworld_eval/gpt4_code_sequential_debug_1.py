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
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()
        self.font = pygame.font.Font(None, 24)

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        new_circle = Circle(color)
        while pygame.sprite.spritecollideany(new_circle, self.circles) is not None:
            new_circle.reset()
        self.circles.add(new_circle)

    def update_circles(self):
        for circle in list(pygame.sprite.spritecollide(self.agent, self.circles, True)):
            if circle.color == GREEN:
                self.score += 1
            elif circle.color == RED:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))
        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True
        
        self.circles.update()

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
            if not self.game_over:
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        self.agent.draw(self.screen)
        self.circles.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            self.show_message('Game Over! Press R to restart.')
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        message_surface = font.render(message, True, BLUE)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
        self.render_game()
        self.clock.tick(FPS)


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, key):
        direction_key_mapping = {
            pygame.K_LEFT: (-GRID_SIZE, 0),
            pygame.K_RIGHT: (GRID_SIZE, 0),
            pygame.K_UP: (0, -GRID_SIZE),
            pygame.K_DOWN: (0, GRID_SIZE),
        }
        direction = direction_key_mapping.get(key)
        if direction:
            self.rect.x += direction[0]
            self.rect.y += direction[1]
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.direction = random.choice([(GRID_SIZE, 0), (-GRID_SIZE, 0),(0, GRID_SIZE), (0, -GRID_SIZE)])

    def update(self):
        if random.randrange(100) < 2:  # 2% chance to move
            self.rect.x += self.direction[0]
            self.rect.y += self.direction[1]
            # Keep circle within the window
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
            # Change direction if it hits a wall
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.direction = (self.direction[0] * -1, self.direction[1])
            if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
                self.direction = (self.direction[0], self.direction[1] * -1)


if __name__ == "__main__":
    game = Game()
    while True:
        event = pygame.event.poll()
        if not game.run(event):
            break
    pygame.quit()

