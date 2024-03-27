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

    def turn(self, direction):
        opposite_dirs = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if direction != opposite_dirs[self.direction]:
            self.direction = direction

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

    def collision_with_boundaries(self):
        x, y = self.body[0]
        return x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT

    def collision_with_self(self):
        return self.body[0] in self.body[1:]


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = self.randomize_position()
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def randomize_position(self):
        return (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

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

    def run(self):
        for event in pygame.event.get():
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

        self.snake.move()
        if self.snake.collision_with_boundaries() or self.snake.collision_with_self():
            self.game_over = True
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.food = Food()
        self.screen.fill(pygame.Color('black'))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, pygame.Color('red'), self.food.rect)
        score_text = self.font.render(f'Score: {self.snake.length - 1}', True, pygame.Color('white'))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        self.clock.tick(10)
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to Restart', True, pygame.Color('white'))
            self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))
            pygame.display.flip()
            while self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.reset_game()
                        self.game_over = False
                        return True
                    elif event.type == pygame.QUIT:
                        return False
        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()

