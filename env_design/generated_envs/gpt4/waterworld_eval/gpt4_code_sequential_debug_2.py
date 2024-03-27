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

    def spawn_initial_circles(self):
        for _ in range((GRID_WIDTH * GRID_HEIGHT) // 40):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        collision = True
        while collision:
            circle.rect.center = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE + CIRCLE_RADIUS,
                                  random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE + CIRCLE_RADIUS)
            if pygame.sprite.spritecollideany(circle, self.circles) is None:
                collision = False
        self.circles.add(circle)

    def update_circles(self):
        for circle in list(self.circles):
            if self.agent.rect.colliderect(circle.rect):
                if circle.color == GREEN:
                    self.score += 1
                elif circle.color == RED:
                    self.score -= 1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([GREEN, RED]))

        if len([circle for circle in self.circles if circle.color == GREEN]) == 0:
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
            self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        for circle in self.circles:
            circle.move_smoothly()
            circle.draw(self.screen)
        self.agent.draw(self.screen)
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            self.show_message('Game Over! Press R to restart.', 36)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont(None, size)
        message_surface = font.render(message, True, BLUE)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            keys = pygame.key.get_pressed()
            self.agent.move(keys)
            self.update_circles()
        self.render_game()
        return event.type != pygame.QUIT


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def move(self, keys):
        direction = pygame.Vector2(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
                                   keys[pygame.K_DOWN] - keys[pygame.K_UP])
        if direction.length_squared() != 0:
            direction = direction.normalize()
        self.rect.move_ip(direction * 5)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        if self.direction.length_squared() != 0:
            self.direction = self.direction.normalize()

    def move_smoothly(self):
        self.rect.move_ip(self.direction * 1)
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).contains(self.rect):
            self.direction *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
