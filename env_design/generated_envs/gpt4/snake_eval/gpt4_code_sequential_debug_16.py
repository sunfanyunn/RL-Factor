import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
GRID_SIZE = 20

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.length = 1
        self.surf = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.surf.fill((0, 255, 0))
        self.game_over = False

    def update(self):
        if not self.game_over:
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
            if (x, y) in self.body or x < 0 or y < 0 or x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT:
                self.game_over = True
            else:
                self.body.insert(0, new_head)
                if len(self.body) > self.length:
                    self.body.pop()

    def grow(self):
        self.length += 1

    def set_direction(self, new_direction):
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite[self.direction]:
            self.direction = new_direction

    def draw(self, screen):
        for segment in self.body:
            screen.blit(self.surf, segment)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.surf = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.surf.fill((255, 0, 0))

    def respawn(self):
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE

    def draw(self, screen):
        screen.blit(self.surf, (self.x, self.y))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.set_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        self.snake.set_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        self.snake.set_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.snake.set_direction('RIGHT')

            self.snake.update()
            if self.snake.game_over:
                break

            if self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.grow()
                self.food.respawn()
                self.score += 1

            self.screen.fill((0, 0, 0))
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            # Display the score
            font = pygame.font.SysFont(None, 35)
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (5, 5))

            pygame.display.flip()
            self.clock.tick(10)

    def show_game_over(self):
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render('Game Over! Score: {} Press any key to restart.'.format(self.score), True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        # restart the event loop to avoid having a queue full of KEYDOWN event
        pygame.event.clear()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    self.reset_game()

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        game.run()
        if game.game_over:
            game.show_game_over()
    pygame.quit()
