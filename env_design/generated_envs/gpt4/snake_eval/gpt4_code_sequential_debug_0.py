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
        self.direction = 'UP'
        self.length = 1  # New attribute to track length
    
    def grow(self):
        self.length += 1  # Increment the snake's length

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

        # Only keep the snake's body up to its current length
        while len(self.body) > self.length:
            self.body.pop()

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], GRID_SIZE, GRID_SIZE))


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.randomize_position()

    def randomize_position(self):
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, GRID_SIZE, GRID_SIZE))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0  # Initialize score

    def run(self, event):
        if not self.game_over:
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

            if self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.grow()
                self.food.randomize_position()
                self.score += 1  # Update the score

            head = self.snake.body[0]
            if (
                head[0] < 0 or head[0] >= SCREEN_WIDTH or
                head[1] < 0 or head[1] >= SCREEN_HEIGHT or
                head in self.snake.body[1:]
            ):
                self.game_over = True

        self.draw_game()
        self.clock.tick(10)

    def draw_game(self):
        self.screen.fill((0,0,0))
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        score_text = 'Score: ' + str(self.score)
        score_surf = self.font.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))
        if self.game_over:
            game_over_text = 'Game Over! Press any key to restart'
            game_over_surf = self.font.render(game_over_text, True, (255, 255, 255))
            game_over_rect = game_over_surf.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(game_over_surf, game_over_rect)
        pygame.display.flip()

    def restart(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.reset_game()
                return True
        return not self.game_over

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif game.game_over:
                running = game.restart()
            else:
                game.run(event)
    pygame.quit()


