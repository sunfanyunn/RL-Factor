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
        self.circles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        while True:
            potential_position = (random.randrange(GRID_WIDTH) * GRID_SIZE, random.randrange(GRID_HEIGHT) * GRID_SIZE)
            circle.rect.topleft = potential_position
            if not pygame.sprite.spritecollideany(circle, self.all_sprites):
                break
        self.circles.add(circle)
        self.all_sprites.add(circle)

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_rect(self.agent, circle):
                self.score += 1 if circle.color == GREEN else -1
                circle.kill()
                self.spawn_circle(random.choice([GREEN, RED]))
        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        for circle in self.circles:
            circle.kill()
        self.circles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
            self.reset_game()
        return True

    def render_game(self):
        self.screen.fill(WHITE)
        score_text = self.font.render('Score: {}'.format(self.score), True, (0, 0, 0))
        self.screen.blit(score_text, (5, 5))
        self.all_sprites.draw(self.screen)
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', 36)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        if not self.handle_events(event):
            return False
        if not self.game_over:
            self.agent.update()
            self.circles.update()
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
        if direction == 'UP' and self.rect.top > 0:
            self.rect.y -= GRID_SIZE
        elif direction == 'DOWN' and self.rect.bottom < HEIGHT:
            self.rect.y += GRID_SIZE
        elif direction == 'LEFT' and self.rect.left > 0:
            self.rect.x -= GRID_SIZE
        elif direction == 'RIGHT' and self.rect.right < WIDTH:
            self.rect.x += GRID_SIZE

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move('UP')
        elif keys[pygame.K_DOWN]:
            self.move('DOWN')
        elif keys[pygame.K_LEFT]:
            self.move('LEFT')
        elif keys[pygame.K_RIGHT]:
            self.move('RIGHT')


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        direction = random.choice([(0, GRID_SIZE), (0, -GRID_SIZE), (GRID_SIZE, 0), (-GRID_SIZE, 0)])
        self.rect.move_ip(*direction)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game.run(event):
                running = False
    pygame.quit()
