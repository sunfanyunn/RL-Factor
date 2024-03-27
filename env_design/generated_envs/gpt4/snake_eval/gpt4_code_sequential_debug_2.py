import pygame
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_SIZE = 20
SNAKE_SPEED = 10


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.length = 1  # Added line for length initialization
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

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

        new_head_pos = (head_x, head_y)

        if (new_head_pos[0] < 0 or new_head_pos[0] >= SCREEN_WIDTH or
                new_head_pos[1] < 0 or new_head_pos[1] >= SCREEN_HEIGHT or
                new_head_pos in self.body[1:]):
            return True
        self.body.insert(0, new_head_pos)
        if len(self.body) > self.length:
            self.body.pop()
        return False

    def draw(self, screen):
        for segment in self.body:
            snake_rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            screen.blit(self.image, snake_rect)


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 35)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self):
        for event in pygame.event.get():  # Modified to get all events
            if event.type == pygame.QUIT:
                return False
            if not self.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                    self.snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                    self.snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                    self.snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                    self.snake.direction = 'RIGHT'

        if not self.game_over:
            self.game_over = self.snake.update()
            if (self.snake.body[0][0] == self.food.x and self.snake.body[0][1] == self.food.y):
                self.snake.length += 1
                self.score += 1
                self.food = Food()

            self.screen.fill((0, 0, 0))
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.display_score()
            pygame.display.update()
            self.clock.tick(SNAKE_SPEED)
        else:
            self.display_game_over()
            for event in pygame.event.get():  # Added for restart check
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()

        return True

    def display_game_over(self):
        text = self.font.render('Game Over! Press R to restart', True, (255, 255, 255))
        self.screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
