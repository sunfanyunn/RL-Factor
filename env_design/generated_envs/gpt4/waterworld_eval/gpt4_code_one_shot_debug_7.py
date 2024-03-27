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
        self.circles = pygame.sprite.Group()
        self.agent = Agent()
        self.all_sprites = pygame.sprite.Group(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle.rect.topleft = self.position_circle()
        self.circles.add(circle)
        self.all_sprites.add(circle)

    def position_circle(self):
        while True:
            pos_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            pos_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if not any(sprite.rect.collidepoint((pos_x, pos_y)) for sprite in self.all_sprites):
                return pos_x, pos_y

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                elif circle.color == RED:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(random.choice([GREEN, RED]))
        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.all_sprites.empty()
        self.circles.empty()
        self.agent.reset()
        self.spawn_initial_circles()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True

    def render_game(self):
        self.screen.fill(WHITE)
        if self.game_over:
            self.show_message("Game Over!", 40)
        else:
            self.all_sprites.draw(self.screen)
            score_text = 'Score: ' + str(self.score)
            font = pygame.font.Font(None, 36)
            text = font.render(score_text, True, (0, 0, 0))
            self.screen.blit(text, (10, 10))
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        text = font.render(message, True, WHITE, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        if not self.handle_events():
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
        x, y = direction
        self.rect.x = min(max(self.rect.x + x, 0), WIDTH - self.rect.width)
        self.rect.y = min(max(self.rect.y + y, 0), HEIGHT - self.rect.height)

    def update(self):
        keys = pygame.key.get_pressed()
        direction = [0, 0]
        if keys[pygame.K_UP]:
            direction[1] = -GRID_SIZE
        if keys[pygame.K_DOWN]:
            direction[1] = GRID_SIZE
        if keys[pygame.K_LEFT]:
            direction[0] = -GRID_SIZE
        if keys[pygame.K_RIGHT]:
            direction[0] = GRID_SIZE
        self.move(direction)


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
        directions = [(GRID_SIZE, 0), (-GRID_SIZE, 0), (0, GRID_SIZE), (0, -GRID_SIZE)]
        direction = random.choice(directions)
        self.rect.x = (self.rect.x + direction[0]) % WIDTH
        self.rect.y = (self.rect.y + direction[1]) % HEIGHT

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
