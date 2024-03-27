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
            color = GREEN if _ < 5 else RED
            self.spawn_circle(color)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle.reset()
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.reset()
        self.circles.add(circle)

    def update_circles(self):
        green_circles = [circle for circle in self.circles if circle.color == GREEN]
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                    green_circles.remove(circle)
                elif circle.color == RED:
                    self.score -= 1
                circle.reset()
                self.spawn_circle(random.choice([GREEN, RED]))

        if not green_circles:
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
        self.agent.update()
        self.agent.draw(self.screen)
        self.circles.update()
        self.circles.draw(self.screen)
        self.update_circles()

        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Score: {self.score}', True, BLUE)
        text_rect = text.get_rect(top=10, left=10)
        self.screen.blit(text, text_rect)

        if self.game_over:
            self.show_message("Game Over!")

        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont(None, size)
        text = font.render(message, True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.render_game()
        else:
            self.show_message("Press 'R' to restart!", size=24)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
        self.clock.tick(FPS)
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.radius = CIRCLE_RADIUS

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

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.radius = CIRCLE_RADIUS
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def reset(self):
        self.rect.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def update(self):
        self.move_smoothly()
        if random.randint(0, 20) == 0:
            self.direction = random.choice(['up', 'down', 'left', 'right'])

    def move_smoothly(self):
        dx, dy = 0, 0
        if self.direction == 'up' and self.rect.top > 0:
            dy = -GRID_SIZE // 10
        elif self.direction == 'down' and self.rect.bottom < HEIGHT:
            dy = GRID_SIZE // 10
        elif self.direction == 'left' and self.rect.left > 0:
            dx = -GRID_SIZE // 10
        elif self.direction == 'right' and self.rect.right < WIDTH:
            dx = GRID_SIZE // 10
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

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

