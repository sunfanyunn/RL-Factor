import pygame
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
    
    def check_collision(self):
        head_x, head_y = self.body[0]
        for segment in self.body[1:]:
            if head_x == segment[0] and head_y == segment[1]:
                return True
        return head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT
    
    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, GRID_SIZE, GRID_SIZE))


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = (random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (*self.position, GRID_SIZE, GRID_SIZE))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
    
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
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
                self.game_over = self.snake.check_collision()
                if self.snake.body[0] == self.food.position:
                    self.snake.grow()
                    self.food = Food()
                    self.score += 1
                self.screen.fill((0, 0, 0))
                self.snake.draw(self.screen)
                self.food.draw(self.screen)
                score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))
                pygame.display.flip()
                self.clock.tick(10)
            else:
                self.show_game_over()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
        return True

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 90)
        text = font.render('Game Over! Press R to restart', True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()


