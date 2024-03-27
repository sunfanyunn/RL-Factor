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
        self.direction = 'UP'
        self.length = 1
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=self.body[0])

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

    def turn(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def grow(self):
        self.length += 1


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    @staticmethod
    def randomize_position():
        columns = SCREEN_WIDTH // GRID_SIZE
        rows = SCREEN_HEIGHT // GRID_SIZE
        return random.randint(0, columns - 1) * GRID_SIZE, random.randint(0, rows - 1) * GRID_SIZE


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        food_pos = Food.randomize_position()
        self.food = Food(*food_pos)

    def run(self, event):
        if not self.game_over:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.turn('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.turn('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.turn('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn('RIGHT')

            self.update_game()
            self.draw_game()
            pygame.display.flip()
            self.clock.tick(10)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

        return True

    def update_game(self):
        self.snake.update()
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            food_pos = Food.randomize_position()
            self.food = Food(*food_pos)

        head_x, head_y = self.snake.body[0]
        if (
            head_x < 0 or
            head_y < 0 or
            head_x >= SCREEN_WIDTH or
            head_y >= SCREEN_HEIGHT or
            self.snake.body[0] in self.snake.body[1:]
        ):
            self.game_over = True

    def draw_game(self):
        self.screen.fill((0, 0, 0))
        for segment in self.snake.body:
            self.screen.blit(self.snake.image, segment)

        self.screen.blit(self.food.image, (self.food.x, self.food.y))

        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f'Score: {self.snake.length-1}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            font = pygame.font.SysFont('Arial', 35)
            game_over_text = font.render('Game Over! Press R to Play Again', True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
