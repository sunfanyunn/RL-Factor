
import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.length = 1


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.myfont = pygame.font.SysFont('monospace', 16)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.food = Food(x, y)

    def run(self, event):
        while not self.game_over:
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
            self.update_snake()
            self.check_collisions()
            self.draw_elements()
            self.clock.tick(10)  # Control the frame rate
        self.show_game_over()
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
            pygame.display.update()
            self.clock.tick(10)
        return True

    def update_snake(self):
        head_x, head_y = self.snake.body[0]
        if self.snake.direction == 'UP':
            head_y -= GRID_SIZE
        elif self.snake.direction == 'DOWN':
            head_y += GRID_SIZE
        elif self.snake.direction == 'LEFT':
            head_x -= GRID_SIZE
        elif self.snake.direction == 'RIGHT':
            head_x += GRID_SIZE
        new_head = (head_x, head_y)
        self.snake.body.insert(0, new_head)
        if new_head == (self.food.x, self.food.y):
            self.score += 1
            self.spawn_food()
        else:
            self.snake.body.pop()

    def check_collisions(self):
        head_x, head_y = self.snake.body[0]
        # Check if snake collides with walls
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            self.game_over = True
        # Check if snake collides with itself
        for segment in self.snake.body[1:]:
            if segment == self.snake.body[0]:
                self.game_over = True

    def draw_elements(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black color
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)
        score_text = self.myfont.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))
        pygame.display.update()

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        go_font = pygame.font.SysFont('monospace', 50)
        go_text = go_font.render('Game Over!', True, (255, 255, 255))
        self.screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - go_text.get_height() // 2))
        restart_text = self.myfont.render('Press R to Restart', True, (255, 255, 255))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
