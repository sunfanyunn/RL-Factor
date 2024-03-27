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
        self.font = pygame.font.Font(None, 28)
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(RED)
            self.spawn_circle(GREEN)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle.reset()
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.reset()
        self.circles.add(circle)

    def update_circles(self):
        green_circles_count = 0
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                    green_circles_count += 1
                    circle.kill()
                    self.spawn_circle(GREEN)
                elif circle.color == RED:
                    self.score -= 1
                    circle.kill()
                    self.spawn_circle(RED)

        if green_circles_count == 10:
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
            if event.key == pygame.K_r:
                self.reset_game()
            else:
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.update()
        self.circles.draw(self.screen)
        self.agent.update()
        self.screen.blit(self.agent.image, self.agent.rect)
        score_text = self.font.render('Score: ' + str(self.score), True, BLUE)
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', size=50)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        message_surface = font.render(message, True, BLUE)
        x = (WIDTH - message_surface.get_width()) // 2
        y = (HEIGHT - message_surface.get_height()) // 2
        self.screen.blit(message_surface, (x, y))

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
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.radius = CIRCLE_RADIUS

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction_key):
        offset = {pygame.K_UP: (0, -GRID_SIZE), pygame.K_DOWN: (0, GRID_SIZE),
                  pygame.K_LEFT: (-GRID_SIZE, 0), pygame.K_RIGHT: (GRID_SIZE, 0)}
        if direction_key in offset:
            direction = offset[direction_key]
            self.rect.move_ip(direction)
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.radius = CIRCLE_RADIUS

    def reset(self):
        self.rect.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        x_dir = random.choice([-1, 0, 1])
        y_dir = random.choice([-1, 0, 1])
        x = x_dir * random.randint(0, GRID_SIZE // 4)
        y = y_dir * random.randint(0, GRID_SIZE // 4)
        self.rect.move_ip(x, y)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()

