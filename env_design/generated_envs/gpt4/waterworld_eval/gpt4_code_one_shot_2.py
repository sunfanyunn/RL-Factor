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
        self.agent_group = pygame.sprite.Group(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            circle = Circle(color)
            circle.rect.topleft = pos
            if pygame.sprite.spritecollide(circle, self.circles, False) == []:
                self.circles.add(circle)
                break

    def update_circles(self):
        for circle in pygame.sprite.groupcollide(self.circles, self.agent_group, True, False):
            if circle.color == GREEN:
                self.score += 1
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))

    def reset_game(self):
        self.score = 0
        self.circles.empty()
        self.agent.reset()
        self.spawn_initial_circles()
        self.game_over = False

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
        return True

    def render_game(self):
        self.screen.fill(WHITE)
        self.agent_group.draw(self.screen)
        self.circles.draw(self.screen)
        self.show_message(f'Score: {self.score}', 20, (10, 10))
        if self.game_over:
            self.show_message("Game Over!", 48, (WIDTH // 2, HEIGHT // 2))
        pygame.display.flip()

    def show_message(self, message, size, position):
        font = pygame.font.Font(None, size)
        text_surface = font.render(message, True, BLUE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = position
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.agent.move()
            self.circles.update()
            self.update_circles()
            green_circles = [circle for circle in self.circles if circle.color == GREEN]
            if not green_circles:
                self.game_over = True
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
        self.speed = 5

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x = max(self.rect.x - self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.x = min(self.rect.x + self.speed, WIDTH - self.rect.width)
        if keys[pygame.K_UP]:
            self.rect.y = max(self.rect.y - self.speed, 0)
        if keys[pygame.K_DOWN]:
            self.rect.y = min(self.rect.y + self.speed, HEIGHT - self.rect.height)

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])
        self.speed = 2

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.direction = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])

    def update(self):
        self.move_smoothly()
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])

    def move_smoothly(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
