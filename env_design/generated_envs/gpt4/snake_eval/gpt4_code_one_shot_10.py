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
        """
        Initialize the snake's body, direction and image.
        self.body should be a list of tuples representing the snake's body segments (top-left coordinates)
        self.direction should be one of {\"UP\", \"DOWN\", \"LEFT\", \"RIGHT\"}
        self.length should be an integer representing the length of the snake
        """
        super().__init__()
        self.body = [(100, 100)]
        self.direction = \"UP\"


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize the food's position and image.
        self.x and self.y should be the top-left coordinate of the food
        self.rect should be a pygame.Rect object with the initial position of the food
        """
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)


class Game:
    """
    The main class for the Snake game.
    """
    def __init__(self):
        """
        Initialize the game and its components.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.reset_game()

    def reset_game(self):
        """
        Reset the game to its initial state.
        self.game_over is a boolean representing whether the game is over
        self.snake is a Snake object representing the snake character
        self.food is a Food object representing the active food item (randomize the food location)
        """
        self.game_over = False
        self.snake = Snake()
        self.food = Food(random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                        random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)
        self.score = 0

    def run(self, event):
        """
        Please implement the main game loop here.
        Use self.clock.tick(10) to set a maximum frame rate.
        """
        self.clock.tick(10)
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            self.handle_input(event)
            self.update_game()
            self.check_collisions()
            self.draw_elements()
        else:
            self.show_game_over()

        pygame.display.update()
        return True

    def handle_input(self, event):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.snake.direction != 'DOWN':
            self.snake.direction = 'UP'
        elif key[pygame.K_DOWN] and self.snake.direction != 'UP':
            self.snake.direction = 'DOWN'
        elif key[pygame.K_LEFT] and self.snake.direction != 'RIGHT':
            self.snake.direction = 'LEFT'
        elif key[pygame.K_RIGHT] and self.snake.direction != 'LEFT':
            self.snake.direction = 'RIGHT'

    def update_game(self):
        head_x, head_y = self.snake.body[0]
        if self.snake.direction == 'UP':
            head_y -= GRID_SIZE
        elif self.snake.direction == 'DOWN':
            head_y += GRID_SIZE
        elif self.snake.direction == 'LEFT':
            head_x -= GRID_SIZE
        elif self.snake.direction == 'RIGHT':
            head_x += GRID_SIZE

        new_head = (head_x, head_y)
        self.snake.body.insert(0, new_head)
        if new_head == (self.food.x, self.food.y):
            self.score += 1
            self.spawn_food()
        else:
            self.snake.body.pop()

    def check_collisions(self):
        head_x, head_y = self.snake.body[0]
        if (head_x < 0 or head_y < 0 or
                head_x >= SCREEN_WIDTH or head_y >= SCREEN_HEIGHT or
                self.snake.body[0] in self.snake.body[1:]):
            self.game_over = True

    def draw_elements(self):
        self.screen.fill(pygame.Color('black'))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, pygame.Color('red'), self.food.rect)
        score_text = self.font.render(f'Score: {self.score}', True, pygame.Color('white'))
        self.screen.blit(score_text, (5, 5))

    def spawn_food(self):
        self.food = Food(random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                        random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

    def show_game_over(self):
        game_over_text = self.font.render('GAME OVER! Press any key to restart.', True, pygame.Color('white'))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        key = pygame.key.get_pressed()
        if any(key):
            self.reset_game()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
