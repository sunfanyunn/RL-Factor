
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

        new_head = (x, y)

        # Move body
        self.body = [new_head] + self.body[:-1]

        # Check for collision with self
        if self.body[0] in self.body[1:]:
            return True

        # Check for collision with walls
        if (x < 0 or y < 0 or x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT):
            return True

        return False

    def grow(self):
        self.body.append(self.body[-1])
        self.length += 1

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != 'DOWN':
                self.direction = 'UP'
            elif event.key == pygame.K_DOWN and self.direction != 'UP':
                self.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                self.direction = 'RIGHT'


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.Font(None, 36)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
        if self.game_over:
            self.show_game_over()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
        else:
            self.snake.handle_keys(event)
            game_over = self.snake.update()

            if game_over:
                self.game_over = True
                return not self.game_over

            if self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.grow()
                self.score += 1
                self.food = Food()

            self.screen.fill((0, 0, 0))
            self.draw_snake()
            self.draw_food()
            self.show_score()
            pygame.display.flip()
            self.clock.tick(10)

        return not self.game_over

    def draw_snake(self):
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def draw_food(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

    def show_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (50, 50))

    def show_game_over(self):
        game_over_text = self.font.render('Game Over! Press R to Restart', True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
