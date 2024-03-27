
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
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle_created = False
        while not circle_created:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle = Circle(color)
            new_circle.rect.topleft = (x, y)
            if not any(sprite.rect.colliderect(new_circle.rect) for sprite in self.circles):
                self.circles.add(new_circle)
                circle_created = True

    def update_circles(self):
        for circle in self.circles:
            if self.agent.rect.colliderect(circle.rect):
                self.score += 1 if circle.color == GREEN else -1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([GREEN, RED]))
        green_circles = sum(1 for circle in self.circles if circle.color == GREEN)
        if green_circles == 0:
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
        return True

    def render_game(self):
        self.screen.fill(WHITE)
        for circle in self.circles:
            self.screen.blit(circle.image, circle.rect)
        self.screen.blit(self.agent.image, self.agent.rect)
        score_text = f'Score: {self.score}'
        self.show_message(score_text, 24, (5, 5))
        if self.game_over:
            self.show_message("Game Over!", 36, (WIDTH // 2, HEIGHT // 2))
        pygame.display.flip()

    def show_message(self, message, size=36, position=(0, 0)):
        font = pygame.font.SysFont("Arial", size)
        text_surface = font.render(message, True, BLUE)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        if not self.handle_events(event):
            return False
        if not self.game_over:
            self.agent.move(event)
            self.update_circles()
            self.render_game()
        self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect.x -= GRID_SIZE
            elif event.key == pygame.K_RIGHT:
                self.rect.x += GRID_SIZE
            elif event.key == pygame.K_UP:
                self.rect.y -= GRID_SIZE
            elif event.key == pygame.K_DOWN:
                self.rect.y += GRID_SIZE

            self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_smoothly()

    def reset(self):
        new_position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.rect.topleft = new_position
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

