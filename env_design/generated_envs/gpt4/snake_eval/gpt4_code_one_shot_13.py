import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = 'RIGHT'
        self.length = 1

    def move(self):
        x, y = self.body[0]
        if self.direction == 'UP':
            y -= GRID_SIZE
        elif self.direction == 'DOWN':
            y += GRID_SIZE
        elif self.direction == 'LEFT':
            x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            x += GRID_SIZE
        new_head = (x, y)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def eat(self):
        self.length += 1

    def get_head_position(self):
        return self.body[0]

    def collided_with_self(self):
        return self.get_head_position() in self.body[1:]

    def collided_with_boundaries(self):
        x, y = self.get_head_position()
        return x < 0 or y < 0 or x >= SCREEN_WIDTH or y >= SCREEN_HEIGHT

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = self.spawn_food()
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def spawn_food(self):
        return (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

    def relocate(self):
        self.x, self.y = self.spawn_food()
        self.rect.topleft = (self.x, self.y)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 35)
        self.score = 0
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_snake()
            self.check_collision()
            self.draw_objects()
        else:
            self.show_game_over()
        pygame.display.update()
        self.clock.tick(10)
        return True

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            if event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            if event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            if event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'
            if event.key == pygame.K_r:
                self.reset_game()

    def update_snake(self):
        self.snake.move()

    def check_collision(self):
        if self.snake.get_head_position() == (self.food.x, self.food.y):
            self.score += 1
            self.snake.eat()
            self.food.relocate()
        if self.snake.collided_with_self() or self.snake.collided_with_boundaries():
            self.game_over = True

    def draw_objects(self):
        self.screen.fill((0, 0, 0))
        for x, y in self.snake.body:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x, y, GRID_SIZE, GRID_SIZE))
        self.food.draw(self.screen)
        score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, [0, 0])

    def show_game_over(self):
        game_over_text = self.font.render('GAME OVER!', True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, game_over_rect)
        restart_text = self.font.render('Press R to Restart', True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.run(event)
    pygame.quit()