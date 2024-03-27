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
        self.body = [(100, 100)]
        self.direction = "UP"
        self.length = 1

    def update(self):
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

    def grow(self):
        self.length += 1

    def check_collision(self):
        head = self.body[0]
        # Check if head collides with body
        if head in self.body[1:]:
            return True
        # Check if head collides with boundaries
        x, y = head
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return True

        return False


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def respawn(self):
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.rect.x = self.x
        self.rect.y = self.y


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
        self.font = pygame.font.SysFont(None, 36)

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        # Draw food
        pygame.draw.rect(self.screen, pygame.Color('red'), self.food.rect)

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, pygame.Color('white'))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                        self.snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                        self.snake.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                        self.snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                        self.snake.direction = 'RIGHT'

            self.snake.update()
            if self.snake.check_collision():
                self.game_over = True

            if self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.grow()
                self.food.respawn()
                self.score += 1

            self.draw()

            self.clock.tick(10)

        # Display game over message
        game_over_text = self.font.render('Game Over! Press R to Restart', True, pygame.Color('white'))
        self.screen.fill(pygame.Color('black'))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        waiting_for_reset = True
        while waiting_for_reset:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting_for_reset = False

        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
