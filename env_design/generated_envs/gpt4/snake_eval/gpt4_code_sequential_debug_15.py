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

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == 'LEFT':
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == 'RIGHT':
            new_head = (head_x + GRID_SIZE, head_y)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def turn(self, dir):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if dir != opposite_directions[self.direction]:
            self.direction = dir

    def grow(self):
        self.length += 1

    def check_collision(self):
        head = self.body[0]
        if (head[0] >= SCREEN_WIDTH or head[0] < 0 or
                head[1] >= SCREEN_HEIGHT or head[1] < 0):
            return True
        if head in self.body[1:]:
            return True
        return False

    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (0, 255, 0), rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = (random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                          random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, (223, 163, 49), self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
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
            self.check_food_collision()
            if self.snake.check_collision():
                self.game_over = True
            self.screen.fill((0, 0, 0))
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.show_score()
            pygame.display.flip()
            self.clock.tick(10)
        else:
            self.show_game_over()
            return self.check_restart_event(event)
        return True

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

    def check_food_collision(self):
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.food = Food()
            self.score += 1

    def show_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = 'Score: ' + str(self.score)
        text_surface = font.render(score_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (5, 5))

    def show_game_over(self):
        font = pygame.font.SysFont(None, 75)
        text_surface = font.render('Game Over!', True, (255, 255, 255))
        rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text_surface, rect)

        font_small = pygame.font.SysFont(None, 30)
        text_surface_small = font_small.render('Press R to Restart', True, (255, 255, 255))
        rect_small = text_surface_small.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(text_surface_small, rect_small)

    def check_restart_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()
            return True
        return False


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    