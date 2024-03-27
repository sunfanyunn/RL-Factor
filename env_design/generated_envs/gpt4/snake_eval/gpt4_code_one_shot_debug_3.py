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
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def collides_with_walls(self):
        x, y = self.body[0]
        return x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

    def spawn(self):
        self.x = random.randint(0, SCREEN_WIDTH - GRID_SIZE)
        self.y = random.randint(0, SCREEN_HEIGHT - GRID_SIZE)
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food(random.randint(0, SCREEN_WIDTH - GRID_SIZE),
                         random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
        self.score = 0

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                    self.snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                    self.snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                    self.snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                    self.snake.direction = 'RIGHT'
            self.snake.update()
            self.check_collision()
            self.draw_elements()
            self.clock.tick(10)
            return not self.game_over

    def check_collision(self):
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.score += 1
            self.snake.grow()
            self.food.spawn()
        if self.snake.collides_with_self() or self.snake.collides_with_walls():
            self.game_over = True

    def draw_elements(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black color
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)
        go_font = pygame.font.SysFont('monospace', 16)
        go_text = go_font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(go_text, (5, 5))
        if self.game_over:
            go_font = pygame.font.SysFont('monospace', 50)
            go_text = go_font.render('Game Over!', True, (255, 255, 255))
            restart_text = go_font.render('Press R to Restart', True, (255, 255, 255))
            self.screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - go_text.get_height() // 2))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                            SCREEN_HEIGHT // 2 - restart_text.get_height() // 2 + 50))
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
    pygame.quit()
