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
        self.all_sprites = pygame.sprite.Group(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle.reset()
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.reset()
        self.circles.add(circle)
        self.all_sprites.add(circle)

    def update_circles(self):
        for circle in list(self.circles):
            if not self.game_over:
                circle.update()
            if self.agent.rect.colliderect(circle.rect):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                self.spawn_circle(random.choice([RED, GREEN]))
                circle.kill()
        self.game_over = self.check_game_over()

    def reset_game(self):
        self.score = 0
        self.agent.reset()
        for circle in list(self.circles):
            circle.kill()
        self.spawn_initial_circles()
        self.game_over = False

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            elif not self.game_over:
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        if self.game_over:
            self.show_message('Game Over! Press R to restart', 36, (WIDTH // 2, HEIGHT // 2), True)
        else:
            score_text = f'Score: {self.score}'
            self.show_message(score_text, 20, (5, 5), False)
        pygame.display.flip()

    def show_message(self, message, size, position, center):
        font = pygame.font.Font(None, size)
        text_surface = font.render(message, True, WHITE)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
            self.agent.update()
        self.render_game()
        self.clock.tick(FPS)

    def check_game_over(self):
        return not any(circle.color == GREEN for circle in self.circles)


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, direction):
        move_map = {
            pygame.K_UP: (0, -GRID_SIZE),
            pygame.K_DOWN: (0, GRID_SIZE),
            pygame.K_LEFT: (-GRID_SIZE, 0),
            pygame.K_RIGHT: (GRID_SIZE, 0)
        }
        if direction in move_map:
            dx, dy = move_map[direction]
            self.rect.x += dx
            self.rect.y += dy


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
        move_map = {
            'UP': (0, -GRID_SIZE),
            'DOWN': (0, GRID_SIZE),
            'LEFT': (-GRID_SIZE, 0),
            'RIGHT': (GRID_SIZE, 0)
        }
        if self.direction in move_map:
            dx, dy = move_map[self.direction]
            self.rect.x += dx
            self.rect.y += dy
            
            # Change direction if the circle hits a wall
            if self.rect.left < 0 or self.rect.right > WIDTH:
                dx = -dx
            if self.rect.top < 0 or self.rect.bottom > HEIGHT:
                dy = -dy
            # Update the direction to reflect the bounce
            inv_map = {v: k for k, v in move_map.items()}
            self.direction = inv_map[(dx, dy)]


if __name__ == '__main__':
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

