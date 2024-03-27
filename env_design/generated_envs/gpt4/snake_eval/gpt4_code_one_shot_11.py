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
        self.direction = "RIGHT"
        self.length = 1

    def turn(self, direction):
        if direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
        elif direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"

    def move(self):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= GRID_SIZE
        elif self.direction == "DOWN":
            y += GRID_SIZE
        elif self.direction == "LEFT":
            x -= GRID_SIZE
        elif self.direction == "RIGHT":
            x += GRID_SIZE

        new_head = (x, y)

        # Check for collision with boundaries
        if (x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT or new_head in self.body):
            return True

        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

        return False

    def grow(self):
        self.length += 1


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    @staticmethod
    def spawn_food():
        return Food(random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                    random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food.spawn_food()

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
            return True

        # Event Handling
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.turn("UP")
            elif event.key == pygame.K_DOWN:
                self.snake.turn("DOWN")
            elif event.key == pygame.K_LEFT:
                self.snake.turn("LEFT")
            elif event.key == pygame.K_RIGHT:
                self.snake.turn("RIGHT")

        # Move Snake
        if self.snake.move():
            self.game_over = True

        # Check if Snake has eaten the food
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.score += 1
            self.food = Food.spawn_food()

        self.screen.fill((0, 0, 0))

        # Draw Snake
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        # Draw Food
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

        # Display Score
        font = pygame.font.SysFont(None, 35)
        score_text = font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, [0, 0])

        pygame.display.flip()
        self.clock.tick(10)

        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        running = game.run(event)
    pygame.quit()
