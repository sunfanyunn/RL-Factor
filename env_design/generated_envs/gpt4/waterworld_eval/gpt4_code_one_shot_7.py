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
        for _ in range(5):  # Adjust number to spawn more or fewer circles
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        circle_rect = circle.image.get_rect()
        while True:
            pos_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            pos_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            circle_rect.topleft = (pos_x, pos_y)
            if not any(sprite.rect.colliderect(circle_rect) for sprite in self.all_sprites):
                break
        circle.rect.topleft = (pos_x, pos_y)
        self.circles.add(circle)
        self.all_sprites.add(circle)

    def update_circles(self):
        red_circles = [circle for circle in self.circles if circle.color == RED]
        green_circles = [circle for circle in self.circles if circle.color == GREEN]
        for circle in self.circles:
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                circle.kill()
                new_color = random.choice([GREEN, RED])
                self.spawn_circle(new_color)
                if not green_circles:
                    self.game_over = True

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.agent.reset()
        self.circles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.agent)
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
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            keys = pygame.key.get_pressed()
            direction = pygame.math.Vector2(0, 0)
            if keys[pygame.K_UP]:
                direction.y = -1
            elif keys[pygame.K_DOWN]:
                direction.y = 1
            elif keys[pygame.K_LEFT]:
                direction.x = -1
            elif keys[pygame.K_RIGHT]:
                direction.x = 1
            self.agent.move(direction)
            self.circles.update()
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

    def move(self, direction):
        self.rect.move_ip(direction.x * GRID_SIZE, direction.y * GRID_SIZE)

    def update(self):
        self.rect.clamp_ip(self.image.get_rect(topleft=(0, 0), size=(WIDTH, HEIGHT)))


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

    def reset(self, color=None):
        if color:
            self.color = color
            pygame.draw.circle(
                self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
            )

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dir_x, dir_y = random.choice(directions)
        self.rect.move_ip(dir_x * (CIRCLE_RADIUS // 2), dir_y * (CIRCLE_RADIUS // 2))
        self.rect.clamp_ip(self.image.get_rect(topleft=(0, 0), size=(WIDTH, HEIGHT)))


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

