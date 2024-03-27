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
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
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
        return (head in self.body[1:] or
                head[0] < 0 or head[0] >= SCREEN_WIDTH or
                head[1] < 0 or head[1] >= SCREEN_HEIGHT)

    def change_direction(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions[self.direction] and new_direction in opposite_directions:
            self.direction = new_direction


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = self.randomize_position()

    def randomize_position(self):
        return (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 35)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self):
        while not self.game_over and not pygame.event.peek(pygame.QUIT):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction('RIGHT')

            self.snake.update()
            if self.snake.check_collision():
                self.game_over = True

            if (self.snake.body[0][0], self.snake.body[0][1]) == (self.food.x, self.food.y):
                self.snake.grow()
                self.food.x, self.food.y = self.food.randomize_position()
                self.score += 1

            self.screen.fill(pygame.Color('black'))
            for segment in self.snake.body:
                pygame.draw.rect(self.screen, pygame.Color('green'),
                                 (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.screen, pygame.Color('red'),
                             (self.food.x, self.food.y, GRID_SIZE, GRID_SIZE))

            score_text = self.font.render(f'Score: {self.score}', True, pygame.Color('white'))
            self.screen.blit(score_text, (10, 10))

            if self.game_over:
                game_over_text = self.font.render('Game Over! Press R to Restart', True, pygame.Color('white'))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                waiting_for_restart = True
                while waiting_for_restart:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                self.reset_game()
                                waiting_for_restart = False
                            elif event.key == pygame.K_ESCAPE:
                                waiting_for_restart = False
                                self.game_over = True

            pygame.display.update()
            self.clock.tick(10)

        return not self.game_over


if __name__ == '__main__':
    game = Game()
    while True:
        if not game.run():
            break
    pygame.quit()
