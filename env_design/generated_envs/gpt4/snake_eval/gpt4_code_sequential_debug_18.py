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
        self.body = [(100, 100)]
        self.direction = "UP"
        self.length = 1

    def move(self):
        x, y = self.body[0]
        if self.direction == 'UP':
            self.body.insert(0, (x, y - GRID_SIZE))
        elif self.direction == 'DOWN':
            self.body.insert(0, (x, y + GRID_SIZE))
        elif self.direction == 'LEFT':
            self.body.insert(0, (x - GRID_SIZE, y))
        elif self.direction == 'RIGHT':
            self.body.insert(0, (x + GRID_SIZE, y))
        
        if len(self.body) > self.length:
            self.body.pop()

    def turn(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def grow(self):
        self.length += 1

    def check_collision(self):
        x, y = self.body[0]
        if x < 0 or y < 0 or x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT or self.body[0] in self.body[1:]:
            return True
        return False


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.randomize_position()

    def randomize_position(self):
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont('Arial', 35)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if self.game_over and event.key == pygame.K_r:
                self.reset_game()
            elif not self.game_over:
                if event.key == pygame.K_UP:
                    self.snake.turn('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.turn('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.turn('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn('RIGHT')

    def run(self, event):
        self.handle_events(event)

        if self.game_over:
            text = self.game_font.render('Game Over! Press R to restart', True, (255,255,255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            return True

        self.snake.move()

        if self.snake.check_collision():
            self.game_over = True

        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.food.randomize_position()
            self.score += 1

        self.screen.fill((0,0,0))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        self.food.draw(self.screen)
        score_text = self.game_font.render(f'Score: {self.score}', True, (255,255,255))
        self.screen.blit(score_text, [0, 0])
        pygame.display.update()

        self.clock.tick(10)
        return True


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
    


