import pygame
import random

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        self.direction = "RIGHT"
        self.body = [(self.rect.x, self.rect.y)]
        self.snake_length = 1

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        self.direction = "RIGHT"
        self.body = [(self.rect.x, self.rect.y)]
        self.snake_length = 1

    def update(self):
        if len(self.body) > self.snake_length:
            del self.body[0]
        if self.direction == "RIGHT":
            self.rect.x += GRID_SIZE
        elif self.direction == "LEFT":
            self.rect.x -= GRID_SIZE
        elif self.direction == "UP":
            self.rect.y -= GRID_SIZE
        elif self.direction == "DOWN":
            self.rect.y += GRID_SIZE
        self.body.append((self.rect.x, self.rect.y))

    def change_direction(self, new_direction):
        if new_direction == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if new_direction == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if new_direction == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if new_direction == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    def check_collision(self):
        if (
            self.rect.left < 0
            or self.rect.right > WIDTH
            or self.rect.top < 0
            or self.rect.bottom > HEIGHT
        ):
            return True
        if len(self.body) > 1 and self.body[-1] in self.body[:-1]:
            return True
        return False

    def grow(self):
        self.snake_length += 1


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.topleft = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.win_message = False

        self.all_sprites = pygame.sprite.Group()
        self.snake = Snake()
        self.food = Food()
        self.all_sprites.add(self.snake, self.food)

        self.reset_button = pygame.Rect(20, 20, 100, 50)
        self.reset_button_active = False

    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        self.win_message = False

    def render_game(self):
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        for segment in self.snake.body:
            pygame.draw.rect(
                self.screen,
                BLACK,
                pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE),
            )
        if self.win_message:
            self.show_message("You Win!")
        elif self.game_over:
            self.show_message("Game Over.")
            self.reset_button_active = True
        else:
            self.reset_button_active = False

        pygame.draw.rect(self.screen, BLACK, self.reset_button)
        self.show_message(
            "Reset", 32, self.reset_button.x + 20, self.reset_button.y + 10
        )

        pygame.display.flip()
        self.clock.tick(FPS)

    def show_message(self, message, size=36, x=None, y=None):
        font = pygame.font.Font(None, size)
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect()
        if x is not None and y is not None:
            text_rect.topleft = (x, y)
        else:
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.screen.blit(text, text_rect)

    def run(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.reset_button_active and self.reset_button.collidepoint(
                    event.pos
                ):
                    self.reset_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")

        self.snake.update()
        if self.snake.rect.colliderect(self.food.rect):
            self.snake.grow()
            self.food.randomize_position()

        if len(self.snake.body) == GRID_WIDTH * GRID_HEIGHT:
            self.win_message = True

        if self.snake.check_collision() or self.win_message:
            self.game_over = True
        self.render_game()
        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()