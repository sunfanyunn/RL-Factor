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
        self.all_sprites = pygame.sprite.Group(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle_added = False
        while not circle_added:
            circle.reset()
            circle_added = pygame.sprite.spritecollideany(circle, self.all_sprites) is None
        self.all_sprites.add(circle)
        self.circles.add(circle)

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_mask(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                elif circle.color == RED:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(random.choice([RED, GREEN]))
        self.game_over = not any(circle.color == GREEN for circle in self.circles)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        for circle in list(self.circles):
            circle.kill()
        self.spawn_initial_circles()
        self.agent.reset()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            else:
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.show_message('Score: ' + str(self.score))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', center=True)
        pygame.display.flip()

    def show_message(self, message, size=36, center=False):
        font = pygame.font.Font(None, size)
        text_surface = font.render(message, True, BLUE)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = self.screen.get_rect().center
        else:
            text_rect.topleft = (10, 10)
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.agent.update()
            self.update_circles()
            self.circles.update()
        self.render_game()
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, key):
        step_size = GRID_SIZE
        if key == pygame.K_LEFT and self.rect.left > 0:
            self.rect.x -= step_size
        elif key == pygame.K_RIGHT and self.rect.right < WIDTH:
            self.rect.x += step_size
        elif key == pygame.K_UP and self.rect.top > 0:
            self.rect.y -= step_size
        elif key == pygame.K_DOWN and self.rect.bottom < HEIGHT:
            self.rect.y += step_size

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS), random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS))

    def update(self):
        if not self.rect:
            return
        step_size = random.randint(1, GRID_SIZE // 2)
        direction_x = random.choice([-1, 1])
        direction_y = random.choice([-1, 1])
        if self.rect.right + step_size * direction_x >= WIDTH:
            direction_x *= -1
        if self.rect.left + step_size * direction_x <= 0:
            direction_x *= -1
        if self.rect.bottom + step_size * direction_y >= HEIGHT:
            direction_y *= -1
        if self.rect.top + step_size * direction_y <= 0:
            direction_y *= -1
        self.rect.x += step_size * direction_x
        self.rect.y += step_size * direction_y


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
