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
BLACK = (0, 0, 0)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WaterWorld Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.circles = pygame.sprite.Group()
        self.agent = Agent()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        num_circles = GRID_WIDTH * GRID_HEIGHT // 10
        for _ in range(num_circles // 2):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        collision = True
        while collision:
            collision = False
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle = Circle(color)
            new_circle.rect.topleft = (x, y)
            if pygame.sprite.spritecollideany(new_circle, self.circles):
                collision = True
            else:
                self.circles.add(new_circle)

    def update_circles(self):
        for circle in self.circles:
            circle.move_smoothly()
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                elif circle.color == RED:
                    self.score -= 1
                self.circles.remove(circle)
                color = GREEN if random.choice([True, False]) else RED
                self.spawn_circle(color)
        self.circles.update()

        remaining_green = any(c.color == GREEN for c in self.circles)
        if not remaining_green:
            self.game_over = True

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.circles.empty()
        self.agent.reset()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()
        self.agent.move(event)

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.show_message(f'Score: {self.score}', size=20, position=(10, 10))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', size=36, position=(WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

    def show_message(self, message, size=36, position=(WIDTH // 2, HEIGHT // 2)):
        font = pygame.font.Font(None, size)
        text_surface = font.render(message, True, BLACK)
        rect = text_surface.get_rect()
        rect.center = position
        self.screen.blit(text_surface, rect)

    def run(self, event):
        if not self.handle_events(event):
            return False
        self.update_circles()
        self.render_game()
        self.clock.tick(FPS)
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = GRID_SIZE

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.rect.left > 0:
                self.rect.x -= self.speed
            if event.key == pygame.K_RIGHT and self.rect.right < WIDTH:
                self.rect.x += self.speed
            if event.key == pygame.K_UP and self.rect.top > 0:
                self.rect.y -= self.speed
            if event.key == pygame.K_DOWN and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def reset(self):
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.rect.topleft = (x, y)

    def update(self):
        pass

    def move_smoothly(self):
        self.rect.x += random.choice([-1, 0, 1])
        self.rect.y += random.choice([-1, 0, 1])
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
