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


class WaterWorldGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WaterWorld Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0  # New score variable
        self.win_message = False

        self.all_sprites = pygame.sprite.Group()
        self.agent = Agent()
        self.circles = pygame.sprite.Group()

        self.spawn_initial_circles()

        self.all_sprites.add(self.agent, self.circles)

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)

        for _ in range(5):
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        while pygame.sprite.spritecollide(circle, self.all_sprites, False):
            circle.reset()
        self.circles.add(circle)
        self.all_sprites.add(
            circle
        )  # Add this line to update the circle after resetting

    def update_circles(self):
        collisions = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collisions:
            if circle.color == GREEN:
                self.score += 1  # Positive reward for capturing a green circle
            elif circle.color == RED:
                self.score -= 1  # Negative reward for hitting a red circle
            self.spawn_circle(random.choice([RED, GREEN]))

        if not any(circle.color == GREEN for circle in self.circles.sprites()):
            self.win_message = True

    def reset_game(self):
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()
        self.game_over = False
        self.win_message = False
        self.score = 0  # Reset score

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.reset_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.agent.move("RIGHT")
                    elif event.key == pygame.K_LEFT:
                        self.agent.move("LEFT")
                    elif event.key == pygame.K_UP:
                        self.agent.move("UP")
                    elif event.key == pygame.K_DOWN:
                        self.agent.move("DOWN")

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        # Display the score on the screen
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            self.show_message("Game Over. Click or press 'R' to restart.")
        elif self.win_message:
            self.show_message("You Win! Click or press 'R' to restart.")
        else:
            pygame.display.flip()
            self.clock.tick(FPS)

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self):
        while True:
            self.handle_events()
            self.agent.update()
            self.circles.update()
            self.update_circles()

            if not any(circle.color == GREEN for circle in self.circles.sprites()):
                self.win_message = True

            self.render_game()


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
        if direction == "RIGHT" and self.rect.right < WIDTH:
            self.rect.x += GRID_SIZE
        elif direction == "LEFT" and self.rect.left > 0:
            self.rect.x -= GRID_SIZE
        elif direction == "UP" and self.rect.top > 0:
            self.rect.y -= GRID_SIZE
        elif direction == "DOWN" and self.rect.bottom < HEIGHT:
            self.rect.y += GRID_SIZE

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
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.reset()

    def reset(self):
        self.position = [
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        ]
        self.rect.topleft = self.position
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        speed = GRID_SIZE / FPS

        dx = self.direction[0] * speed
        dy = self.direction[1] * speed

        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        if not (0 <= new_x <= WIDTH - CIRCLE_RADIUS * 2):
            self.direction[0] *= -1
        if not (0 <= new_y <= HEIGHT - CIRCLE_RADIUS * 2):
            self.direction[1] *= -1

        self.position = [new_x, new_y]
        self.rect.x = round(new_x)
        self.rect.y = round(new_y)


if __name__ == "__main__":
    game = WaterWorldGame()
    game.run()
