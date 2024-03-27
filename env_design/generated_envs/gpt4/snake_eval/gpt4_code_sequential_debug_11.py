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
        self.direction = 'RIGHT'
        self.length = 1

    def turn(self, new_direction):
        allowed_moves = {'UP': ['LEFT', 'RIGHT'],
                         'DOWN': ['LEFT', 'RIGHT'],
                         'LEFT': ['UP', 'DOWN'],
                         'RIGHT': ['UP', 'DOWN']}
        if new_direction in allowed_moves[self.direction]:
            self.direction = new_direction

    def move(self):
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

    def render(self, screen):
        for segment in self.body:
            segment_rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), segment_rect)

    def has_collided_with_itself(self):
        head = self.body[0]
        return head in self.body[1:]

    def has_collided_with_wall(self):
        head = self.body[0]
        return head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 35)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.snake.move()
            self.check_collisions()
            self.render()
            pygame.display.flip()
            self.clock.tick(10)
        return not self.game_over

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                self.snake.turn('UP')
            elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                self.snake.turn('DOWN')
            elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                self.snake.turn('LEFT')
            elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                self.snake.turn('RIGHT')
            elif event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def check_collisions(self):
        if self.snake.has_collided_with_wall() or self.snake.has_collided_with_itself():
            self.game_over = True
        head_x, head_y = self.snake.body[0]
        if pygame.Rect(head_x, head_y, GRID_SIZE, GRID_SIZE).colliderect(self.food.rect):
            self.snake.grow()
            self.food = Food()
            self.score += 1

    def render(self):
        self.screen.fill((0, 0, 0))
        self.snake.render(self.screen)
        self.food.render(self.screen)
        self.show_score()
        if self.game_over:
            self.show_game_over()

    def show_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_game_over(self):
        game_over_text = self.font.render('GAME OVER! Press R to restart or ESC to exit', True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, game_over_rect)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.run(pygame.event.poll())
    pygame.quit()
    sys.exit()

