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
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(GRID_WIDTH * GRID_HEIGHT // 4):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle.reset()
        while pygame.sprite.spritecollide(circle, self.all_sprites, False):
            circle.reset()
        self.circles.add(circle)
        self.all_sprites.add(circle)

    def update_circles(self):
        for circle in self.circles:
            if pygame.sprite.collide_circle(self.agent, circle):
                self.score += 1 if circle.color == GREEN else -1
                color = GREEN if random.choice([True, False]) else RED
                circle.color = color
                circle.reset()
        self.circles.update()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        for circle in self.circles:
            circle.kill()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            elif not self.game_over:
                if event.key == pygame.K_UP:
                    self.agent.move((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.agent.move((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.agent.move((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.agent.move((1, 0))
        return True

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        if self.game_over:
            self.show_message("Game Over!")
        else:
            self.update_circles()
        self.show_score()
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.screen.blit(text_surface, text_rect)

    def show_score(self):
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render('Score: ' + str(self.score), True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.render_game()
            self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, direction):
        x, y = direction
        self.rect.x += x * GRID_SIZE
        self.rect.y += y * GRID_SIZE
        self.rect.x = max(min(self.rect.x, WIDTH - CIRCLE_RADIUS * 2), 0)
        self.rect.y = max(min(self.rect.y, HEIGHT - CIRCLE_RADIUS * 2), 0)

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.rect = self.image.get_rect()

    def reset(self):
        self.rect.x = random.randrange(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS, GRID_SIZE)
        self.rect.y = random.randrange(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS, GRID_SIZE)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        dx, dy = self.direction
        self.rect.x += dx
        self.rect.y += dy
        # Change direction if hitting bounds
        if self.rect.x <= 0 or self.rect.x >= WIDTH - CIRCLE_RADIUS * 2:
            self.direction = (-dx, dy)
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - CIRCLE_RADIUS * 2:
            self.direction = (dx, -dy)

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
