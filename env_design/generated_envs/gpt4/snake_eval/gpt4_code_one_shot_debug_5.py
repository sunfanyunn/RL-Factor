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
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(pygame.Color('green'))
        self.rect = pygame.Rect(self.body[0][0], self.body[0][1], GRID_SIZE, GRID_SIZE)
    
    def update(self):
        if self.direction == "UP":
            new_head = (self.body[0][0], self.body[0][1] - GRID_SIZE)
        elif self.direction == "DOWN":
            new_head = (self.body[0][0], self.body[0][1] + GRID_SIZE)
        elif self.direction == "LEFT":
            new_head = (self.body[0][0] - GRID_SIZE, self.body[0][1])
        elif self.direction == "RIGHT":
            new_head = (self.body[0][0] + GRID_SIZE, self.body[0][1])

        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

        self.rect = pygame.Rect(new_head[0], new_head[1], GRID_SIZE, GRID_SIZE)

    def grow(self):
        self.length += 1
    
    def head_collides_with_body(self):
        return self.body[0] in self.body[1:]
    
    def head_collides_with_wall(self):
        return self.rect.x < 0 or self.rect.y < 0 or self.rect.right > SCREEN_WIDTH or self.rect.bottom > SCREEN_HEIGHT


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(pygame.Color('red'))
        self.randomize_position()

    def randomize_position(self):
        cols = SCREEN_WIDTH // GRID_SIZE
        rows = SCREEN_HEIGHT // GRID_SIZE
        self.x = random.randint(0, cols - 1) * GRID_SIZE
        self.y = random.randint(0, rows - 1) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()

    def run(self, event=None):
        if self.game_over:
            if event and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
        else:
            self.handle_events(event)
            self.snake.update()
            self.check_collision()
            self.draw()
            self.clock.tick(10)
        return not self.game_over

    def handle_events(self, event):
        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'

    def check_collision(self):
        if self.snake.head_collides_with_wall() or self.snake.head_collides_with_body():
            self.game_over = True
        elif self.snake.rect.colliderect(self.food.rect):
            self.snake.grow()
            self.food.randomize_position()

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for segment in self.snake.body:
            seg_rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            self.screen.blit(self.snake.image, seg_rect)

        self.screen.blit(self.food.image, self.food.rect)

        score_text = self.font.render(f'Score: {self.snake.length - 1}', True, pygame.Color('white'))
        self.screen.blit(score_text, (5, 5))

        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to Restart', True, pygame.Color('white'))
            game_over_center = (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2)
            self.screen.blit(game_over_text, game_over_center)

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
    pygame.quit()
