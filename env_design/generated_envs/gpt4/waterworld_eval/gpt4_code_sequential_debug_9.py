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
        pygame.display.set_caption("Dynamic Environment Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.SysFont('arial', 25)
        self.agent = Agent(self.screen)
        self.circles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.agent)
        self.green_circles = 0
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle.rect.topleft = self.rand_position()
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.rect.topleft = self.rand_position()
        self.circles.add(circle)
        self.all_sprites.add(circle)
        if color == GREEN:
            self.green_circles += 1

    def rand_position(self):
        return random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                    self.green_circles -= 1
                elif circle.color == RED:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(random.choice([RED, GREEN]))
        if self.green_circles <= 0:
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.green_circles = 0
        self.agent.reset()
        self.circles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
            self.reset_game()
        directions = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
        }
        if event.type == pygame.KEYDOWN and event.key in directions:
            self.agent.move(directions[event.key])
        return True

    def render_game(self):
        self.screen.fill(WHITE)
        for entity in self.all_sprites:
            self.screen.blit(entity.image, entity.rect)
        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            self.show_message("Game Over! Press 'R' to restart.")
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont('arial', size)
        message_surface = font.render(message, True, RED)
        message_rect = message_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        running = self.handle_events(event)
        if running:
            if not self.game_over:
                self.agent.update()
                self.update_circles()
            self.render_game()
        self.clock.tick(FPS)
        return running


class Agent(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen = screen

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        dx, dy = direction
        self.rect.x += dx * GRID_SIZE
        self.rect.y += dy * GRID_SIZE
        self.rect.clamp_ip(self.screen.get_rect())


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.color = color

    def update(self):
        if not pygame.sprite.spritecollideany(self, self.circles):
            self.move_smoothly()

    def move_smoothly(self):
        vec = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
        vec = vec.normalize() * random.uniform(0.5, 2.5)
        self.rect.x += vec.x
        self.rect.y += vec.y
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()



