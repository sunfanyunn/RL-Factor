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


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.food = Food(x, y)

    def run(self, event):
        # Event handling
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'

        if self.game_over:
            self.screen.fill((0, 0, 0))
            # Show the 'game over' text
            font = pygame.font.SysFont('arial', 35)
            game_over_surface = font.render('Game Over!', True, (255, 255, 255))
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
            self.screen.blit(game_over_surface, game_over_rect)
            # Show the 'restart' text
            restart_surface = font.render('Press R to Restart', True, (255, 255, 255))
            restart_rect = restart_surface.get_rect()
            restart_rect.midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            self.screen.blit(restart_surface, restart_rect)
            pygame.display.flip()
            # Check for R key to restart
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

            return True

        # Game logic for snake movement
        head_x, head_y = self.snake.body[0]
        if self.snake.direction == 'UP':
            head_y -= GRID_SIZE
        elif self.snake.direction == 'DOWN':
            head_y += GRID_SIZE
        elif self.snake.direction == 'LEFT':
            head_x -= GRID_SIZE
        elif self.snake.direction == 'RIGHT':
            head_x += GRID_SIZE

        # Collision with food
        if head_x == self.food.x and head_y == self.food.y:
            self.snake.length += 1
            self.score += 10
            self.snake.body.append((head_x, head_y))
            # Randomize a new food location
            x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            self.food = Food(x, y)
        else:
            # Move the snake's body
            self.snake.body = [(head_x, head_y)] + self.snake.body[:-1]

        # Collision detection with walls or itself
        if (head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT or
            self.snake.body[0] in self.snake.body[1:]):
            self.game_over = True

        # Drawing everything on the screen
        self.screen.fill((0, 0, 0))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)
        # Show the score
        score_text = 'Score: ' + str(self.score)
        score_surface = font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        self.screen.blit(score_surface, score_rect)

        pygame.display.flip()

        self.clock.tick(10)
        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
