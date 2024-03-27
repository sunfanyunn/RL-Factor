import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define directions
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

# Dictionary that maps keyboard keys to directions
DIRECT_DICT = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT
}

# A map that defines the opposite direction
OPPOSITE_DIRECTION_MAP = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = UP
        self.length = 1
        self.score = 0
        self.grow_to_length = 3

    def update(self):
        head_x, head_y = self.body[0]
        if self.direction == UP:
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == LEFT:
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == RIGHT:
            new_head = (head_x + GRID_SIZE, head_y)

        if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT:
            return True

        if new_head in self.body[1:]:
            return True

        self.body.insert(0, new_head)
        if len(self.body) > self.grow_to_length:
            self.body.pop()

        return False

    def grow(self):
        self.grow_to_length += 1
        self.score += 10

    def change_direction(self, new_direction):
        if new_direction != OPPOSITE_DIRECTION_MAP[self.direction]:
            self.direction = new_direction

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def draw(self, screen):
        food_rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, food_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 35)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in DIRECT_DICT:
                self.snake.change_direction(DIRECT_DICT[event.key])

        if not self.game_over:
            self.game_over = self.snake.update()
            self.check_food_collision()
            self.draw()
            self.clock.tick(10)
        else:
            self.show_game_over()
        return not self.game_over

    def check_food_collision(self):
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.food = Food()

    def draw(self):
        self.screen.fill(BLACK)
        for segment in self.snake.body:
            seg_rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, GREEN, seg_rect)
        self.food.draw(self.screen)
        score_text = self.font.render(f'Score: {self.snake.score}', True, WHITE)
        self.screen.blit(score_text, (5, 5))
        pygame.display.flip()

    def show_game_over(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render('Game Over', True, RED)
        restart_text = self.font.render('Press Enter to restart', True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting_for_key = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        self.reset_game()

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
