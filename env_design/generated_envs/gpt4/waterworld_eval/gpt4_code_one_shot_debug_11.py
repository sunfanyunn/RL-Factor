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
        self.all_sprites = pygame.sprite.Group()
        self.circles = pygame.sprite.Group()
        self.agent = Agent()
        self.all_sprites.add(self.agent)
        self.total_green_circles = 0
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(20):
            color = GREEN if _ < 10 else RED
            if color == GREEN:
                self.total_green_circles += 1
            self.spawn_circle(color)

    def spawn_circle(self, color):
        new_circle = Circle(color)
        collision = True
        while collision:
            new_circle.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            collision = pygame.sprite.spritecollideany(new_circle, self.circles)
        self.circles.add(new_circle)
        self.all_sprites.add(new_circle)

    def update_circles(self):
        self.circles.update()
        collided_circles = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collided_circles:
            if circle.color == GREEN:
                self.score += 1
                self.total_green_circles -= 1
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))
            if self.total_green_circles == 0:
                self.game_over = True

    def reset_game(self):
        self.all_sprites.empty()
        self.circles.empty()
        self.agent.reset()
        self.all_sprites.add(self.agent)
        self.game_over = False
        self.score = 0
        self.total_green_circles = 0
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not self.game_over and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.agent.move(event.key)
            elif event.key == pygame.K_r:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.show_message('Score: ' + str(self.score), 30, (5, 5))
        if self.game_over:
            self.show_message('Game Over!', 60, center=True)
        pygame.display.flip()

    def show_message(self, message, size=36, position=None, center=False):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
        else:
            text_rect.topleft = position
        self.screen.blit(text_surface, text_rect)

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
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        vels = {
            pygame.K_UP: (0, -GRID_SIZE),
            pygame.K_DOWN: (0, GRID_SIZE),
            pygame.K_LEFT: (-GRID_SIZE, 0),
            pygame.K_RIGHT: (GRID_SIZE, 0)
        }
        move = vels.get(direction)
        if move:
            self.rect.x += move[0]
            self.rect.y += move[1]
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        if random.randint(0, 20) == 0:
            self.direction = random.choice(directions)

        delta = {
            pygame.K_UP: (0, -2),
            pygame.K_DOWN: (0, 2),
            pygame.K_LEFT: (-2, 0),
            pygame.K_RIGHT: (2, 0)
        }[self.direction]

        self.rect.move_ip(delta)
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
    pygame.quit()
    sys.exit()