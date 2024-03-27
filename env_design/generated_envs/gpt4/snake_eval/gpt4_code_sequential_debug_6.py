import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_SIZE = 20


class Snake():
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.length = 1
        self.score = 0  # Initialize score

    def get_head_position(self):
        return self.body[0]

    def move(self):
        cur = self.get_head_position()
        x, y = cur
        if self.direction == 'UP':
            new = (x, y - GRID_SIZE)
        elif self.direction == 'DOWN':
            new = (x, y + GRID_SIZE)
        elif self.direction == 'LEFT':
            new = (x - GRID_SIZE, y)
        elif self.direction == 'RIGHT':
            new = (x + GRID_SIZE, y)
        if new in self.body:
            self.reset()
        else:
            self.body.insert(0, new)
            if len(self.body) > self.length:
                self.body.pop()

    def turn(self, direction):
        opp_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if direction not in opp_directions[self.direction]:
            self.direction = direction

    def reset(self):
        self.__init__()

    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (0, 255, 0), rect)


class Food():
    def __init__(self):
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, (255, 0, 0), r)


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont('monospace', 16)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
        if not self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.turn('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.turn('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.turn('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn('RIGHT')
        self.snake.move()
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.snake.score += 1  # Increase score
            self.food.randomize_position()

        x, y = self.snake.get_head_position()
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            self.game_over = True

        if self.game_over:
            self.display_game_over()
        else:
            self.screen.fill((0, 0, 0))
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            # Display the current score
            score_text = self.myfont.render(f'Score: {self.snake.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (5, 10))
            pygame.display.update()

        self.clock.tick(10)

    def display_game_over(self):
        text = self.myfont.render(f'Game Over! Your Score: {self.snake.score}', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        restart_text = self.myfont.render('Press R to Restart', True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text_rect)
        self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

if __name__ == '__main__':
    pygame.display.set_caption('Snake Game')
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game.game_over:
                game.reset_game()
            if not game.game_over:
                game.run(event)

        if game.game_over:
            game.display_game_over()

pygame.quit()

