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
        self.body = [(100, 100)]
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

    def head(self):
        return self.body[0]

    def collision_with_self(self):
        if self.head() in self.body[1:]:
            return True
        return False

    def collision_with_boundaries(self):
        x, y = self.head()
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return True
        return False


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.score = 0

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
            return True

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

        self.snake.update()
        if self.snake.head() == (self.food.x, self.food.y):
            self.snake.grow()
            self.food = Food()
            self.score += 10

        if self.snake.collision_with_self() or self.snake.collision_with_boundaries():
            self.game_over = True

        self.screen.fill((0, 0, 0))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), segment + (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)
        self.draw_score()
        pygame.display.flip()
        self.clock.tick(10)
        return True

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))

        if self.game_over:
            over_text = font.render('Game Over! Press R to restart.', True, (255, 255, 255))
            text_rect = over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(over_text, text_rect)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
