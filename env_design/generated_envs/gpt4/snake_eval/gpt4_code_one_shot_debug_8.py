import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
# every time the snake moves, it should move by this amount
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "UP"
        self.length = 1
        self.head_image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.head_image.fill(pygame.Color('green'))

    def update(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            head_y -= GRID_SIZE
        elif self.direction == 'DOWN':
            head_y += GRID_SIZE
        elif self.direction == 'LEFT':
            head_x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            head_x += GRID_SIZE
        new_head = (head_x, head_y)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def self_collision(self):
        return self.body[0] in self.body[1:]


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self, event):
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

        if self.game_over:
            self.show_game_over()
            return True  # Continue the game loop to allow for restart

        self.snake.update()
        self.check_collision_with_food()
        if self.snake.self_collision() or self.check_collision_with_boundaries():
            self.game_over = True

        self.screen.fill(pygame.Color('black'))
        self.draw_elements()
        pygame.display.flip()
        self.clock.tick(10)
        return True

    def check_collision_with_boundaries(self):
        head_x, head_y = self.snake.body[0]
        return head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT

    def check_collision_with_food(self):
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.food = Food()
            self.score += 1

    def draw_elements(self):
        for segment in self.snake.body:
            segment_rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, pygame.Color('green'), segment_rect)
        self.screen.blit(self.food.image, self.food.rect)
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), 1, pygame.Color('white'))
        self.screen.blit(score_text, (5, 5))

    def show_game_over(self):
        font = pygame.font.Font(None, 36)
        message = font.render('Game Over! Score: ' + str(self.score), 1, pygame.Color('white'))
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.fill(pygame.Color('black'))
        self.screen.blit(message, message_rect)
        restart_message = font.render('Press R to Restart', 1, pygame.Color('white'))
        restart_rect = restart_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_message, restart_rect)
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
                return

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()