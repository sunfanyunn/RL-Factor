import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
GRID_SIZE = 20


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = "UP"


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.SysFont('arial', 35)
        self.score = 0

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
        if not self.game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'

        if self.game_over:
            self.show_game_over_screen()
            pygame.display.flip()
            return True

        self.snake_movement()
        self.check_collisions()
        self.draw_elements()
        pygame.display.flip()
        self.clock.tick(10)
        return not self.game_over

    def snake_movement(self):
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

        if self.snake.body[0] == self.food.rect.topleft:
            self.score += 10
            self.food = Food()
        else:
            self.snake.body.pop()

    def check_collisions(self):
        head_x, head_y = self.snake.body[0]
        if (
            head_x < 0 or head_x >= SCREEN_WIDTH or
            head_y < 0 or head_y >= SCREEN_HEIGHT or
            self.snake.body[0] in self.snake.body[1:]
        ):
            self.game_over = True

    def draw_elements(self):
        self.screen.fill((0, 0, 0))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

        score_text = 'Score: ' + str(self.score)
        score_surface = self.font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        self.screen.blit(score_surface, score_rect)

    def show_game_over_screen(self):
        game_over_surface = self.font.render('Game Over!', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.screen.blit(game_over_surface, game_over_rect)

        restart_surface = self.font.render('Press R to Restart', True, (255, 255, 255))
        restart_rect = restart_surface.get_rect()
        restart_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.screen.blit(restart_surface, restart_rect)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
