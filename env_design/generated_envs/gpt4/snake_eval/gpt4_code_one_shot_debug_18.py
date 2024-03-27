import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
every_time_the_snake_moves = 20


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'

    def move(self):
        x, y = self.body[0]
        if self.direction == 'UP':
            y -= every_time_the_snake_moves
        elif self.direction == 'DOWN':
            y += every_time_the_snake_moves
        elif self.direction == 'LEFT':
            x -= every_time_the_snake_moves
        elif self.direction == 'RIGHT':
            x += every_time_the_snake_moves
        new_head = (x, y)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        x, y = self.body[0]
        return (
            x < 0 or y < 0 or x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT or
            self.body[0] in self.body[1:]
        )


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = (
            random.randrange(0, SCREEN_WIDTH, every_time_the_snake_moves),
            random.randrange(0, SCREEN_HEIGHT, every_time_the_snake_moves)
        )
        self.rect = pygame.Rect(self.x, self.y, every_time_the_snake_moves, every_time_the_snake_moves)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food()

    def detect_food_collision(self):
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.score += 1
            return True
        return False

    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                        self.snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                        self.snake.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                        self.snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                        self.snake.direction = 'RIGHT'

            self.snake.move()
            if self.detect_food_collision():
                self.food = Food()
            if self.snake.check_collision():
                self.game_over = True
                continue

            self.screen.fill((0, 0, 0))
            for segment in self.snake.body:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(*segment, every_time_the_snake_moves, every_time_the_snake_moves))
            pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

            pygame.display.flip()
            self.clock.tick(10)

        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
