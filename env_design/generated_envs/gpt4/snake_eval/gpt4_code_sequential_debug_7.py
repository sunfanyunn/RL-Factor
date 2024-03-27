import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_SIZE = 20
SNAKE_SPEED = 10

# Directions
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define the snake class
class Snake(object):
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def update(self):
        if self.grow:
            self.body.append(self.body[-1])
            self.grow = False

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i-1]

        x, y = self.body[0]
        dx, dy = self.direction
        self.body[0] = (x + dx, y + dy)

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

    def collides_with_itself(self):
        head = self.body[0]
        return head in self.body[1:]

    def collides_with_boundaries(self):
        x, y = self.body[0]
        return x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT

# Define the food class
class Food(object):
    def __init__(self):
        self.position = self.randomize_position()
        self.color = RED

    def randomize_position(self):
        return (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Define the game class
class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def draw_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 10))

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food = Food()
            self.snake.grow = True
            self.score += 1

    def run(self):
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to Restart', True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                if event.type == pygame.QUIT:
                    return False
            pygame.display.flip()

            return True

        self.screen.fill((0, 0, 0))
        self.snake.handle_keys()
        self.snake.update()
        self.check_collision_with_food()

        if self.snake.collides_with_itself() or self.snake.collides_with_boundaries():
            self.game_over = True

        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.draw_score()
        pygame.display.flip()

        self.clock.tick(SNAKE_SPEED)

        return True

    def is_running(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
    sys.exit()