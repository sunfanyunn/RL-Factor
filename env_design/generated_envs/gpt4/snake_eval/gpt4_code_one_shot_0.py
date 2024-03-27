import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
# every time the snake moves, it should move by this amount
GRID_SIZE = 20



class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "UP"
        self.length = 1

    def update(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == "LEFT":
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == "RIGHT":
            new_head = (head_x + GRID_SIZE, head_y)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def check_collision(self):
        head = self.body[0]
        # Check if the snake hits the wall
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True

        # Check if the snake hits itself
        if head in self.body[1:]:
            return True

        return False



class Food(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the food's position and image.
        self.x and self.y should be the top-left coordinate of the food
        self.rect should be a pygame.Rect object with the initial position of the food
        """
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def spawn(self):
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect.x = self.x
        self.rect.y = self.y


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self, event):
        # Handle events
        if event.type == pygame.QUIT:
            return False

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP] and self.snake.direction != "DOWN":
            self.snake.direction = "UP"
        if pressed_keys[pygame.K_DOWN] and self.snake.direction != "UP":
            self.snake.direction = "DOWN"
        if pressed_keys[pygame.K_LEFT] and self.snake.direction != "RIGHT":
            self.snake.direction = "LEFT"
        if pressed_keys[pygame.K_RIGHT] and self.snake.direction != "LEFT":
            self.snake.direction = "RIGHT"

        # Update snake
        self.snake.update()

        # Check collision
        if self.snake.check_collision():
            self.game_over = True
            # Display game over
            self.display_message("Game Over!")
            return True

        # Check if snake eats food
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.food.spawn()
            self.score += 1

        # Game loop
        self.screen.fill((0, 0, 0))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), (*segment, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(text, (0, 0))

        pygame.display.flip()
        self.clock.tick(10)
        # Continue the game
        return True

    def display_message(self, message):
        font = pygame.font.Font(None, 48)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

        self.reset_game()


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

