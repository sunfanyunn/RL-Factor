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
        self.font = pygame.font.SysFont(None, 36)
        self.agent = Agent()
        self.agent_sprite = pygame.sprite.GroupSingle(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.reset()
        self.circles.add(circle)

    def update_circles(self):
        collided_circles = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collided_circles:
            if circle.color == GREEN:
                self.score += 1
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))
        green_circles = [circle for circle in self.circles if circle.color == GREEN]
        if len(green_circles) == 0:
            self.game_over = True
        self.circles.update()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent_sprite.empty()
        self.agent.reset()
        self.agent_sprite.add(self.agent)
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()

    def render_game(self):
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.agent_sprite.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', 50)
        pygame.display.flip()

    def show_message(self, message, size=36):
        message_font = pygame.font.SysFont(None, size)
        message_surface = message_font.render(message, True, BLUE)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        if not event or not self.handle_events(event):
            return True
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.agent.move((0, -1))
            if keys[pygame.K_DOWN]:
                self.agent.move((0, 1))
            if keys[pygame.K_LEFT]:
                self.agent.move((-1, 0))
            if keys[pygame.K_RIGHT]:
                self.agent.move((1, 0))
            self.update_circles()
        self.render_game()
        self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        x_move, y_move = direction
        self.rect.x += x_move * GRID_SIZE
        self.rect.y += y_move * GRID_SIZE
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randrange(0, GRID_WIDTH) * GRID_SIZE
        self.rect.y = random.randrange(0, GRID_HEIGHT) * GRID_SIZE
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        x_move, y_move = self.direction
        self.rect.x += x_move
        self.rect.y += y_move
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        if self.rect.left <= 0 or self.rect.right >= WIDTH or self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event:
            running = game.run(event)
        else:
            running = game.run(None)
    pygame.quit()
