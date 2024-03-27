import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
# every time the snake moves, it should move by this amount
GRID_SIZE = 20


class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'UP'
        self.length = 1

    def move(self):
        x, y = self.body[0]
        if self.direction == 'UP':
            y -= GRID_SIZE
        elif self.direction == 'DOWN':
            y += GRID_SIZE
        elif self.direction == 'LEFT':
            x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            x += GRID_SIZE
        new_head = (x, y)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def check_collision(self):
        head_x, head_y = self.body[0]
        return (head_x < 0 or head_x >= SCREEN_WIDTH or
                head_y < 0 or head_y >= SCREEN_HEIGHT or
                self.body[0] in self.body[1:])

class Food:
    def __init__(self):
        self.x, self.y = self.spawn()
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def spawn(self):
        return (random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def respawn(self):
        self.x, self.y = self.spawn()
        self.rect.topleft = (self.x, self.y)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()

    def run(self):
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

        if not self.game_over:
            self.snake.move()
            if self.snake.check_collision():
                self.game_over = True
            elif self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.grow()
                self.food.respawn()

        self.draw_elements()
        pygame.display.flip()
        self.clock.tick(10)
        return True

    def draw_elements(self):
        self.screen.fill(pygame.Color('black'))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, pygame.Color('red'), self.food.rect)

        if self.game_over:
            font = pygame.font.SysFont('Arial', 35)
            game_over_text = font.render('Game Over!', True, pygame.Color('white'))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            restart_text = font.render('Press R to Restart', True, pygame.Color('white'))
            if self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.grow()
                self.food.respawn()
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        else:
            score_text = pygame.font.SysFont('Arial', 28).render('Score: ' + str(self.snake.length - 1), True, pygame.Color('white'))
            self.screen.blit(score_text, (10, 10))

if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
    sys.exit()