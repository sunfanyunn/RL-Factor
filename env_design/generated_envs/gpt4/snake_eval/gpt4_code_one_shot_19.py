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
        self.direction = 'RIGHT'
        self.length = 1

    def update(self):
        x, y = self.body[0]
        if self.direction == 'UP':
            y -= GRID_SIZE
        elif self.direction == 'DOWN':
            y += GRID_SIZE
        elif self.direction == 'LEFT':
            x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            x += GRID_SIZE
        self.body.insert(0, (x, y))
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def check_collision(self):
        x, y = self.body[0]
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return True
        for segment in self.body[1:]:
            if segment == (x, y):
                return True
        return False


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = (random.randint(0, (SCREEN_WIDTH-GRID_SIZE)//GRID_SIZE)*GRID_SIZE, random.randint(0, (SCREEN_HEIGHT-GRID_SIZE)//GRID_SIZE)*GRID_SIZE)
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('red'), self.rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
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
                break

            if self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.grow()
                self.score += 1
                self.food = Food()

            self.screen.fill(pygame.Color('black'))
            for x, y in self.snake.body:
                pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(x, y, GRID_SIZE, GRID_SIZE))
            self.food.draw(self.screen)

            score_text = self.font.render(f'Score: {self.score}', True, pygame.Color('white'))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(10)

        return False

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
        if game.game_over:
            game_over_text = game.font.render('Game Over! Press R to Restart or Q to Quit', True, pygame.Color('white'))
            game.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.reset_game()
                            running = True
                            waiting = False
                        elif event.key == pygame.K_q:
                            waiting = False
                            running = False

    pygame.quit()

