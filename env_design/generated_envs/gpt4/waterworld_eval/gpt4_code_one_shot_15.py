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
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle.reset()
        self.circles.add(circle)

    def update_circles(self):
        for circle in self.circles:
            if pygame.sprite.collide_circle(self.agent, circle):
                self.score += 1 if circle.color == GREEN else -1
                circle.reset()

    def reset_game(self):
        self.game_over = False
        self.circles.empty()
        self.score = 0
        self.agent.reset()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.agent.move('up')
            elif event.key == pygame.K_DOWN:
                self.agent.move('down')
            elif event.key == pygame.K_LEFT:
                self.agent.move('left')
            elif event.key == pygame.K_RIGHT:
                self.agent.move('right')
            elif event.key == pygame.K_r and self.game_over:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.show_message(f'Score: {self.score}')
        if self.game_over:
            self.show_message('Game Over!', 64)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont('arial', size)
        text_surface = font.render(message, True, BLUE)
        rect = text_surface.get_rect(center=((WIDTH // 2, HEIGHT // 2) if self.game_over else (60, 20)))
        self.screen.blit(text_surface, rect)

    def run(self, event):
        if not self.game_over:
            self.handle_events(event)
            self.agent.update()
            self.update_circles()
            self.render_game()
            self.clock.tick(FPS)
            if self.score < 0 or not any(circle.color == GREEN for circle in self.circles):
                self.game_over = True
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        if direction == 'up' and self.rect.top > 0:
            self.rect.y -= GRID_SIZE
        elif direction == 'down' and self.rect.bottom < HEIGHT:
            self.rect.y += GRID_SIZE
        elif direction == 'left' and self.rect.left > 0:
            self.rect.x -= GRID_SIZE
        elif direction == 'right' and self.rect.right < WIDTH:
            self.rect.x += GRID_SIZE


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def reset(self):
        collision = True
        while collision:
            x = random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS * 2)
            y = random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS * 2)
            self.rect.topleft = (x, y)
            collision = any(sprite.rect.colliderect(self.rect) for sprite in self.groups()[0])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        x_dir, y_dir = random.choice(directions)
        self.rect.x += x_dir
        self.rect.y += y_dir
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x -= x_dir * 2
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.rect.y -= y_dir * 2


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
