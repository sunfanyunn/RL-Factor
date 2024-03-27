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
        self.agent_group = pygame.sprite.Group(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            circle = Circle(color, pos)
            if not pygame.sprite.spritecollideany(circle, self.circles):
                self.circles.add(circle)
                break

    def update_circles(self):
        for circle in list(self.circles):
            circle.update()
            if circle.rect.colliderect(self.agent.rect):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([GREEN, RED]))
                break

    def reset_game(self):
        self.score = 0
        self.circles.empty()
        self.agent.reset()
        self.game_over = False
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            self.agent.move(event)

    def render_game(self):
        self.screen.fill(WHITE)
        self.agent_group.draw(self.screen)
        self.circles.draw(self.screen)
        self.show_message(f'Score: {self.score}', 20, (10, 10))
        if self.game_over:
            self.show_message("Game Over!", 48, (WIDTH // 2, HEIGHT // 2))
        pygame.display.flip()

    def show_message(self, message, size, position):
        font = pygame.font.Font(None, size)
        text_surface = font.render(message, True, BLUE)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.agent.update()
            self.update_circles()
            green_circles = [circle for circle in self.circles if circle.color == GREEN]
            if not green_circles:
                self.game_over = True
        self.render_game()
        self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= GRID_SIZE
        elif keys[pygame.K_RIGHT]:
            self.rect.x += GRID_SIZE
        elif keys[pygame.K_UP]:
            self.rect.y -= GRID_SIZE
        elif keys[pygame.K_DOWN]:
            self.rect.y += GRID_SIZE
        self.rect.x = max(min(self.rect.x, WIDTH - self.rect.width), 0)
        self.rect.y = max(min(self.rect.y, HEIGHT - self.rect.height), 0)

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.rect.x += dx * GRID_SIZE
        self.rect.y += dy * GRID_SIZE
        self.rect.x = max(min(self.rect.x, WIDTH - self.rect.width), 0)
        self.rect.y = max(min(self.rect.y, HEIGHT - self.rect.height), 0)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()
