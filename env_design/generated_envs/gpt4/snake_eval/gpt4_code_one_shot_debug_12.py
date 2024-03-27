import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
GRID_SIZE = 20


class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "RIGHT"
        self.length = 1

    def update(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            head_y -= GRID_SIZE
        elif self.direction == "DOWN":
            head_y += GRID_SIZE
        elif self.direction == "LEFT":
            head_x -= GRID_SIZE
        elif self.direction == "RIGHT":
            head_x += GRID_SIZE
        self.body.insert(0, (head_x, head_y))
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def check_collision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False


class Food:
    def __init__(self):
        self.place_food()

    def place_food(self):
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        pygame.display.set_caption('Snake Game')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                        self.snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                        self.snake.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                        self.snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                        self.snake.direction = 'RIGHT'
                    if self.game_over and event.key == pygame.K_r:
                        self.reset_game()

            if not self.game_over:
                self.snake.update()
                if self.snake.check_collision():
                    self.game_over = True
                head = self.snake.body[0]
                if head == (self.food.rect.x, self.food.rect.y):
                    self.snake.grow()
                    self.score += 10
                    self.food.place_food()

                self.screen.fill((0, 0, 0))
                for segment in self.snake.body:
                    pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

                font = pygame.font.SysFont(None, 36)
                score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
                self.screen.blit(score_text, [10, 10])

                if self.game_over:
                    game_over_text = font.render('Game Over! Press R to Restart', True, (255, 255, 255))
                    self.screen.blit(game_over_text, [SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2])

                pygame.display.flip()
                self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
