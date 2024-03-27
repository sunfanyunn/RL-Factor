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

        if len(self.body) >= self.length:
            self.body.pop()

        self.body.insert(0, new_head)

    def grow(self):
        self.length += 1

    def check_collision(self, width, height):
        head = self.body[0]
        return (head in self.body[1:] or
                head[0] < 0 or head[0] >= width or
                head[1] < 0 or head[1] >= height)


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def relocate(self, width, height):
        self.x = random.randint(0, (width // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (height // GRID_SIZE) - 1) * GRID_SIZE
        self.rect.topleft = (self.x, self.y)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food(random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def run(self, event):
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

        if not self.game_over:
            self.snake.update()
            if self.snake.check_collision(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.game_over = True
            head = self.snake.body[0]
            if head == (self.food.x, self.food.y):
                self.snake.grow()
                self.score += 1
                self.food.relocate(SCREEN_WIDTH, SCREEN_HEIGHT)

            self.screen.fill(pygame.Color('black'))
            for segment in self.snake.body:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.screen, pygame.Color('red'), self.food.rect)
            score_text = self.font.render(f'Score: {self.score}', True, pygame.Color('white'))
            self.screen.blit(score_text, (10, 10))
            pygame.display.flip()

        else:
            game_over_text = self.font.render('Game Over! Press R to Restart', True, pygame.Color('white'))
            self.screen.blit(game_over_text,
                             ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset_game()

        self.clock.tick(10)
        return True


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
