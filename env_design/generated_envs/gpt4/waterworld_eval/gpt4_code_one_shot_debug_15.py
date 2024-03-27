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
        self.circles.add(circle)
        circle.reset()

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                self.score += 1 if circle.color == GREEN else -1
                self.spawn_circle(random.choice([GREEN, RED]))
                circle.kill()

    def reset_game(self):
        self.game_over = False
        self.circles.empty()
        self.score = 0
        self.agent.reset()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
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
        self.show_message(f'Score: {self.score}', 20, (60, 20))
        if self.game_over:
            self.show_message('Game Over!', 64, (WIDTH // 2, HEIGHT // 2))
        pygame.display.flip()

    def show_message(self, message, size=36, position=(WIDTH // 2, HEIGHT // 2)):
        font = pygame.font.SysFont('arial', size)
        text_surface = font.render(message, True, BLUE)
        rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, rect)

    def run(self, event):
        if not self.game_over:
            self.handle_events(event)
            self.circles.update()
            self.agent.update()
            self.update_circles()
            self.render_game()
            self.clock.tick(FPS)
            # Check game over condition
            if self.score < 0 or all(circle.color != GREEN for circle in self.circles):
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

    def update(self):
        pass

class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - CIRCLE_RADIUS * 2)
        self.rect.y = random.randint(0, HEIGHT - CIRCLE_RADIUS * 2)
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        x_dir, y_dir = self.direction
        self.rect.x += x_dir
        self.rect.y += y_dir
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x -= x_dir
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.rect.y -= y_dir
            self.direction = (self.direction[0], -self.direction[1])

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
