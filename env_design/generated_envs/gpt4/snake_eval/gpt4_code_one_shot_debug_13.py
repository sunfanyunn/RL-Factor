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

    def check_collision(self, food):
        if self.body[0] == (food.x, food.y):
            self.grow()
            food.respawn(self)
            return False

        if self.body[0] in self.body[1:]:
            return True

        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True

        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))


class Food(pygame.sprite.Sprite):
    def __init__(self, snake):
        super().__init__()
        self.respawn(snake)

    def respawn(self, snake):
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        # Avoid spawning food on the snake
        if (self.x, self.y) in snake.body:
            self.respawn(snake)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE))


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
        self.food = Food(self.snake)
        self.score = 0

    def run(self, event=None):
        if event and event.type == pygame.QUIT:
            return False

        self.handle_input()

        if not self.game_over:
            self.screen.fill((0, 0, 0))
            self.snake.update()

            collision = self.snake.check_collision(self.food)
            if collision is True:
                self.game_over = True

            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.show_score()

            pygame.display.flip()
            self.clock.tick(10)
        else:
            self.show_game_over()
            if event and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

        return True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.snake.direction != 'DOWN':
            self.snake.direction = 'UP'
        elif keys[pygame.K_DOWN] and self.snake.direction != 'UP':
            self.snake.direction = 'DOWN'
        elif keys[pygame.K_LEFT] and self.snake.direction != 'RIGHT':
            self.snake.direction = 'LEFT'
        elif keys[pygame.K_RIGHT] and self.snake.direction != 'LEFT':
            self.snake.direction = 'RIGHT'

    def show_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_game_over(self):
        game_over_text = self.font.render('GAME OVER', True, (255, 255, 255))
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
            else:
                running = game.run(event)
    pygame.quit()

