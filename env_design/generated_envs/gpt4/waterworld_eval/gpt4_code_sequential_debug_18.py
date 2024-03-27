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
        self.agent_sprite = pygame.sprite.Group(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(3):
            self.spawn_circle(RED)
            self.spawn_circle(GREEN)

    def spawn_circle(self, color):
        new_circle = Circle(color)
        overlapping = True
        while overlapping:
            new_circle.reset()
            overlapping = pygame.sprite.spritecollideany(new_circle, self.circles)
        self.circles.add(new_circle)

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([RED, GREEN]))
            circle.update()

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif not self.game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.agent.move((0, -GRID_SIZE))
            elif event.key == pygame.K_DOWN:
                self.agent.move((0, GRID_SIZE))
            elif event.key == pygame.K_LEFT:
                self.agent.move((-GRID_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                self.agent.move((GRID_SIZE, 0))
            elif event.key == pygame.K_r:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.agent_sprite.draw(self.screen)
        self.show_message('Score: ' + str(self.score), 18, (10, 10))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', 36, (WIDTH // 2, HEIGHT // 2), True)
        pygame.display.flip()

    def show_message(self, message, size=36, position=(0, 0), center=False):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, BLUE)
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
            green_count = sum(1 for circle in self.circles if circle.color == GREEN)
            if green_count == 0:
                self.game_over = True
        self.render_game()
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
        self.rect.x += direction[0]
        self.rect.y += direction[1]
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.radius = CIRCLE_RADIUS
        self.reset()

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def update(self):
        self.move_smoothly()
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def move_smoothly(self):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        self.rect.x += dx * GRID_SIZE // 5
        self.rect.y += dy * GRID_SIZE // 5

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

