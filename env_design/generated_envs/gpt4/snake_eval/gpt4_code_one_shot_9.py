import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
# every time the snake moves, it should move by this amount
GRID_SIZE = 20


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "UP"
        self.length = 1
        self.score = 0
        self.head_img = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.head_img.fill((0, 255, 0))

    def update(self):
        self._move()
        self._check_collisions()

    def _move(self):
        x, y = self.body[0]
        if self.direction == 'UP':
            y -= GRID_SIZE
        elif self.direction == 'DOWN':
            y += GRID_SIZE
        elif self.direction == 'LEFT':
            x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            x += GRID_SIZE
        head = (x, y)
        self.body.insert(0, head)
        if len(self.body) > self.length:
            self.body.pop()

    def _check_collisions(self):
        head = self.body[0]
        x, y = head
        if (x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT or
                self.body[0] in self.body[1:]):
            self.game_over = True

    def draw(self, screen):
        for block in self.body:
            block_rect = pygame.Rect(block[0], block[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), block_rect)

    def grow(self):
        self.length += 1
        self.score += 1

    def get_score(self):
        return self.score

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def respawn(self):
        self.rect.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        if not self.game_over:
            self._handle_input(event)
            self.snake.update()
            self._check_food_collision()
            self._draw()
        else:
            self._display_game_over()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
        self.clock.tick(10)
        return True

    def _handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'

    def _check_food_collision(self):
        if self.snake.body[0] == (self.food.rect.x, self.food.rect.y):
            self.snake.grow()
            self.food.respawn()

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        score_text = self.font.render('Score: ' + str(self.snake.get_score()), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def _display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        restart_text = self.font.render('Press R to Restart', True, (255, 255, 255))
        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text,(SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height()))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + restart_text.get_height()))
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
