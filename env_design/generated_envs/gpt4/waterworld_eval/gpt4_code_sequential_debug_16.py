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
        self.font = pygame.font.SysFont(None, 36)
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        new_circle = Circle(color)
        collision = True
        while collision:
            new_circle.reset()
            collision = pygame.sprite.spritecollideany(new_circle, self.circles)
        self.circles.add(new_circle)
        self.all_sprites.add(new_circle)

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                self.circles.remove(circle)
                self.all_sprites.remove(circle)
                if circle.color == GREEN:
                    self.score += 1
                elif circle.color == RED:
                    self.score -= 1
                self.spawn_circle(random.choice([GREEN, RED]))
        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True

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
            pygame.quit()
            sys.exit()
        elif not self.game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
            else:
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', size=24)
        else:
            self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, BLUE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
            self.all_sprites.update()
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

    def move(self, direction):
        move_map = {
            pygame.K_UP: (0, -GRID_SIZE),
            pygame.K_DOWN: (0, GRID_SIZE),
            pygame.K_LEFT: (-GRID_SIZE, 0),
            pygame.K_RIGHT: (GRID_SIZE, 0)
        }
        if direction in move_map:
            self.rect.move_ip(move_map[direction])
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.radius = CIRCLE_RADIUS
        self.reset()

    def reset(self):
        self.rect.x = random.randrange(GRID_WIDTH) * GRID_SIZE
        self.rect.y = random.randrange(GRID_HEIGHT) * GRID_SIZE

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        delta = GRID_SIZE // 10
        self.rect.x += random.choice([-delta, 0, delta])
        self.rect.y += random.choice([-delta, 0, delta])
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
    pygame.quit()
