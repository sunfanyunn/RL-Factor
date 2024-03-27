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
        self.direction should be one of {"UP", "DOWN", "LEFT", "RIGHT"}
        self.length should be an integer representing the length of the snake
        """
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "UP"
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((0, 255, 0))
        self.length = 1

    def head_position(self):
        return self.body[0]

    def update(self):
        head_x, head_y = self.head_position()
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

    def turn(self, new_direction):
        """Turn the snake to the new direction if it's not directly opposite to the current direction."""
        directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if directions[new_direction] != self.direction:
            self.direction = new_direction

    def grow(self):
        self.length += 1

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.image.get_at((0, 0)), (segment[0], segment[1], GRID_SIZE, GRID_SIZE))


class Food(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the food's position and image.
        self.x and self.y should be the top-left coordinate of the food
        self.rect should be a pygame.Rect object with the initial position of the food
        """
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((255, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Game:
    """
    The main class for the Snake game.
    """
    def __init__(self):
        """
        Initialize the game and its components.
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.SysFont('Arial', 35)
        self.reset_game()

    def reset_game(self):
        """
        Reset the game to its initial state.
        self.game_over is a boolean representing whether the game is over
        self.snake is a Snake object representing the snake character
        self.food is a Food object representing the active food item (randomize the food location)
        self.score should be an integer representing the player's score
        """
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def draw_score(self):
        score_text = self.score_font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))

    def check_collision_with_food(self):
        if self.snake.head_position() == (self.food.x, self.food.y):
            self.snake.grow()
            self.food.randomize_position()
            self.score += 1

    def check_collision_with_boundaries(self):
        head_x, head_y = self.snake.head_position()
        if head_x < 0 or head_y < 0 or head_x >= SCREEN_WIDTH or head_y >= SCREEN_HEIGHT:
            self.game_over = True

    def check_collision_with_self(self):
        if self.snake.head_position() in self.snake.body[1:]:
            self.game_over = True

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.turn('UP')
            elif event.key == pygame.K_DOWN:
                self.snake.turn('DOWN')
            elif event.key == pygame.K_LEFT:
                self.snake.turn('LEFT')
            elif event.key == pygame.K_RIGHT:
                self.snake.turn('RIGHT')
            elif event.key == pygame.K_r and self.game_over:
                self.reset_game()

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_boundaries()
            self.check_collision_with_self()
            self.screen.fill((0, 0, 0))
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.draw_score()
        else:
            game_over_text = self.score_font.render('Game Over! Press R to Play Again', True, (255, 255, 255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.update()
        self.clock.tick(10) # Control the frame rate (snake speed)
        return not self.game_over


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
