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
        """
        Initialize the game window, clock, game_over status, and score.
        Create sprite groups for all game objects.
        agent: The player-controlled sprite.
        circles: A group of all circles in the game.
        
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WaterWorld Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0
        self.font = pygame.font.Font(None, 24)
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        while pygame.sprite.spritecollideany(circle, self.all_sprites):
            circle.reset()
        self.circles.add(circle)
        self.all_sprites.add(circle)

    def update_circles(self):
        to_spawn = None
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                self.score += 1 if circle.color == GREEN else -1
                to_spawn = circle.color
                circle.kill()
        if to_spawn:
            self.spawn_circle(to_spawn)
        self.game_over = all(circle.color != GREEN for circle in self.circles)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        self.circles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()
        elif not self.game_over and event.type == pygame.KEYDOWN:
            self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart')
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        message_surface = font.render(message, True, RED)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
            self.all_sprites.update()
        self.render_game()
        self.clock.tick(FPS)
        return self.running


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
        self.reset()

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, key):
        movemap = {pygame.K_UP: (0, -GRID_SIZE), pygame.K_DOWN: (0, GRID_SIZE), pygame.K_LEFT: (-GRID_SIZE, 0), pygame.K_RIGHT: (GRID_SIZE, 0)}
        dx, dy = movemap.get(key, (0, 0))
        if 0 <= self.rect.x + dx < WIDTH and 0 <= self.rect.y + dy < HEIGHT:
            self.rect.move_ip(dx, dy)

    def update(self):
        pass


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
        self.reset()

    def reset(self):
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, GRID_WIDTH) * GRID_SIZE
        self.rect.y = random.randrange(0, GRID_HEIGHT) * GRID_SIZE

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        dx, dy = random.choice([(0, -1), (-1, 0), (0, 1), (1, 0)])
        self.rect.x += dx * GRID_SIZE
        self.rect.y += dy * GRID_SIZE
        if self.rect.left < 0:
            self.rect.right = WIDTH
        elif self.rect.right > WIDTH:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT
        elif self.rect.bottom > HEIGHT:
            self.rect.top = 0

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
        game.clock.tick(FPS)
    pygame.quit()