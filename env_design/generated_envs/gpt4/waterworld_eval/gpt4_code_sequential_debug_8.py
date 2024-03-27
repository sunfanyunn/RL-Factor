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
        for _ in range(3):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.reset()
        self.circles.add(circle)

    def update_circles(self):
        remaining_green_circles = 0
        for circle in list(self.circles):
            if circle.color == GREEN:
                remaining_green_circles += 1
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([RED, GREEN]))
        if remaining_green_circles == 0:
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
        elif not self.game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.agent.move(-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                self.agent.move(GRID_SIZE, 0)
            elif event.key == pygame.K_UP:
                self.agent.move(0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN:
                self.agent.move(0, GRID_SIZE)
            elif event.key == pygame.K_r:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.agent.draw(self.screen)
        self.show_score()

        if self.game_over:
            self.show_message('Game Over! Press R to Restart')

        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont(None, size)
        message_image = font.render(message, True, RED)
        message_rect = message_image.get_rect()
        message_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.screen.blit(message_image, message_rect)

    def show_score(self):
        font = pygame.font.SysFont(None, 24)
        score_image = font.render(f'Score: {self.score}', True, GREEN)
        score_rect = score_image.get_rect()
        score_rect.topleft = (10, 10)
        self.screen.blit(score_image, score_rect)

    def run(self):
        self.clock.tick(FPS)
        for event in pygame.event.get():
            self.handle_events(event)
        if not self.game_over:
            self.update_circles()
            self.circles.update()
        self.render_game()



class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.radius = CIRCLE_RADIUS
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        direction_x = random.choice([-1, 0, 1]) * GRID_SIZE
        direction_y = random.choice([-1, 0, 1]) * GRID_SIZE
        self.rect.x += direction_x
        self.rect.y += direction_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
