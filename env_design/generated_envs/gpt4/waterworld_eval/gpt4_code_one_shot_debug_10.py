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
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.green_count = 10
        self.red_count = 10
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(self.green_count):
            self.spawn_circle(GREEN)
        for _ in range(self.red_count):
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                              random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                                  random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.circles.add(circle)

    def update_circles(self):
        collided_circle = pygame.sprite.spritecollideany(self.agent, self.circles)
        if collided_circle:
            if collided_circle.color == GREEN:
                self.score += 1
                self.green_count -= 1
            else:
                self.score -= 1
                self.red_count -= 1
            self.circles.remove(collided_circle)
            self.spawn_circle(GREEN if random.randint(0, 1) else RED)
            if self.green_count == 0:
                self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.green_count = 10
        self.red_count = 10
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.agent.move('UP')
            elif event.key == pygame.K_DOWN:
                self.agent.move('DOWN')
            elif event.key == pygame.K_LEFT:
                self.agent.move('LEFT')
            elif event.key == pygame.K_RIGHT:
                self.agent.move('RIGHT')
            elif event.key == pygame.K_r and self.game_over:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect)
        score_text = self.font.render('Score: ' + str(self.score), True, (0, 0, 0))
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message("Game Over!")
        else:
            for circle in self.circles:
                circle.update()
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont(None, size)
        message_surface = font.render(message, True, (0, 0, 0))
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)
        pygame.display.flip()

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
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

    def move(self, direction):
        move_dict = {'UP': (0, -GRID_SIZE), 'DOWN': (0, GRID_SIZE), 'LEFT': (-GRID_SIZE, 0), 'RIGHT': (GRID_SIZE, 0)}
        if direction in move_dict:
            move = move_dict[direction]
            self.rect.x += move[0]
            self.rect.y += move[1]


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        move_dict = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}
        move = move_dict[self.direction]
        self.rect.x += move[0] * GRID_SIZE // 5
        self.rect.y += move[1] * GRID_SIZE // 5
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.rect.x -= move[0] * GRID_SIZE // 5
            self.direction = 'RIGHT' if self.direction == 'LEFT' else 'LEFT'
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.rect.y -= move[1] * GRID_SIZE // 5
            self.direction = 'DOWN' if self.direction == 'UP' else 'UP'

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
