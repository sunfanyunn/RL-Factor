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
        self.direction = 'RIGHT'
        self.length = 1
        self.score = 0
        self.head = pygame.Rect(self.body[0][0], self.body[0][1], GRID_SIZE, GRID_SIZE)

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == 'LEFT':
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == 'RIGHT':
            new_head = (head_x + GRID_SIZE, head_y)
        self.body.insert(0, new_head)
        self.head.update(new_head[0], new_head[1], GRID_SIZE, GRID_SIZE)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1
        self.score += 1


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                    self.snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                    self.snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                    self.snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                    self.snake.direction = 'RIGHT'
                elif event.key == pygame.K_r:
                    self.reset_game()

        return True

    def run(self):
        if not self._handle_events():
            return False
        if self.game_over:
            text = self.font.render('Game Over! Score: {} Press R to Restart'.format(self.snake.score), True, pygame.Color('white'))
            self.screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            return True

        self.snake.move()

        if self.snake.head.colliderect(self.food.rect):
            self.snake.grow()
            self.food = Food()

        head_x, head_y = self.snake.body[0]
        if head_x < 0 or head_y < 0 or head_x >= SCREEN_WIDTH or head_y >= SCREEN_HEIGHT:
            self.game_over = True

        for segment in self.snake.body[1:]:
            if self.snake.head.colliderect(pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)):
                self.game_over = True

        self.screen.fill(pygame.Color('black'))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, pygame.Color('red'), self.food.rect)
        score_text = self.font.render('Score: {}'.format(self.snake.score), True, pygame.Color('white'))
        self.screen.blit(score_text, (5, 5))

        pygame.display.flip()
        self.clock.tick(10)
        return True

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()

