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
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        new_circle = Circle(color)
        collision = True
        while collision:
            new_circle.rect.topleft = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)
            collision = bool(pygame.sprite.spritecollide(new_circle, self.circles, False))
        self.all_sprites.add(new_circle)
        self.circles.add(new_circle)

    def update_circles(self):
        collided_circles = pygame.sprite.spritecollide(self.agent, self.circles, dokill=True)
        for circle in collided_circles:
            if circle.color == GREEN:
                self.score += 1
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))
        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        for sprite in self.all_sprites:
            sprite.kill()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        for entity in self.all_sprites:
            self.screen.blit(entity.image, entity.rect)
        score_text = f'Score: {self.score}'
        self.show_message(score_text, 20, (5, 5))

        if self.game_over:
            self.show_message('Game Over! Press SPACE to restart', 30, (WIDTH//2 - 140, HEIGHT//2))
        pygame.display.flip()

    def show_message(self, message, size, position):
        font = pygame.font.SysFont('Arial', size)
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.all_sprites.update()
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

    def move(self, dx, dy):
        if not self.game_over:
            self.rect.x += dx * GRID_SIZE
            self.rect.y += dy * GRID_SIZE
            self.rect.x = max(self.rect.x, 0)
            self.rect.y = max(self.rect.y, 0)
            self.rect.x = min(self.rect.x, WIDTH - self.rect.width)
            self.rect.y = min(self.rect.y, HEIGHT - self.rect.height)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self.move(1, 0)
        elif keys[pygame.K_UP]:
            self.move(0, -1)
        elif keys[pygame.K_DOWN]:
            self.move(0, 1)


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)
        self.direction = random.choice([(0,1), (1,0), (0,-1), (-1,0)])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
        if self.rect.left < 0 or self.rect.right > WIDTH - CIRCLE_RADIUS * 2:
            self.direction = (-self.direction[0], self.direction[1])
            self.rect.x = max(0, min(self.rect.x, WIDTH - CIRCLE_RADIUS * 2))
        if self.rect.top < 0 or self.rect.bottom > HEIGHT - CIRCLE_RADIUS * 2:
            self.direction = (self.direction[0], -self.direction[1])
            self.rect.y = max(0, min(self.rect.y, HEIGHT - CIRCLE_RADIUS * 2))

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
    pygame.quit()
