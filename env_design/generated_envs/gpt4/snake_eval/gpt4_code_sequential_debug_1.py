import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_SIZE = 20


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "UP"
        self.length = 1
        self.score = 0  # Add a score attribute

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            head_y -= GRID_SIZE
        elif self.direction == 'DOWN':
            head_y += GRID_SIZE
        elif self.direction == 'LEFT':
            head_x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            head_x += GRID_SIZE
        new_head = (head_x, head_y)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def turn(self, new_direction):
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposites.get(self.direction, None):
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(segment, (GRID_SIZE, GRID_SIZE)))


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.randomize_position()

    def randomize_position(self):
        self.x = random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE
        self.y = random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE

    def draw(self, surface):
        food_rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, (255, 0, 0), food_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                # Check for specific keys to restart or quit
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
            return True

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.turn('UP')
            elif event.key == pygame.K_DOWN:
                self.snake.turn('DOWN')
            elif event.key == pygame.K_LEFT:
                self.snake.turn('LEFT')
            elif event.key == pygame.K_RIGHT:
                self.snake.turn('RIGHT')

        self.snake.move()
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.length += 1
            self.snake.score += 1  # Increase the score when the snake eats food
            self.food.randomize_position()

        self.screen.fill((0, 0, 0))
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        # Update the score display to include the current score
        score_text = self.font.render(f'Score: {self.snake.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        self.clock.tick(10)

        head_x, head_y = self.snake.body[0]
        if (
            head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT or
            len(self.snake.body) != len(set(self.snake.body))
        ):
            self.game_over = True
            self.display_game_over()

        return not self.game_over

    def display_game_over(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render('Game Over! Press R to restart or Q to quit', True, (255, 255, 255))
        self.screen.blit(game_over_text, (
            SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()

