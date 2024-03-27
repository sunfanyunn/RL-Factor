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
        circle_created = False
        while not circle_created:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle = Circle(color)
            new_circle.rect.topleft = (x, y)
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                circle_created = True

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                self.score += 1 if circle.color == GREEN else -1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([GREEN, RED]))
        green_circles = sum(1 for circle in self.circles if circle.color == GREEN)
        if green_circles == 0:
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
        elif event.type == pygame.KEYDOWN and not self.game_over:
            if event.key == pygame.K_LEFT:
                self.agent.move([-1, 0])
            elif event.key == pygame.K_RIGHT:
                self.agent.move([1, 0])
            elif event.key == pygame.K_UP:
                self.agent.move([0, -1])
            elif event.key == pygame.K_DOWN:
                self.agent.move([0, 1])
            elif event.key == pygame.K_r:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        for circle in self.circles:
            pygame.draw.circle(self.screen, circle.color, circle.rect.center, CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, BLUE, self.agent.rect.center, CIRCLE_RADIUS)
        self.show_message(f'Score: {self.score}', 20, (10, 10))
        if self.game_over:
            self.show_message("Game Over!", 36, (WIDTH // 2, HEIGHT // 2))
        pygame.display.flip()

    def show_message(self, message, size, position):
        font = pygame.font.SysFont("Arial", size)
        text_surface = font.render(message, True, BLUE)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
            self.agent.update()
            self.render_game()
        self.clock.tick(FPS)



class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.radius = CIRCLE_RADIUS

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        self.rect.x += direction[0] * GRID_SIZE
        self.rect.y += direction[1] * GRID_SIZE
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.radius = CIRCLE_RADIUS

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        self.rect.x += random.choice([-1, 0, 1]) * GRID_SIZE // 10
        self.rect.y += random.choice([-1, 0, 1]) * GRID_SIZE // 10
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
        pygame.display.flip()
        game.clock.tick(FPS)
    pygame.quit()