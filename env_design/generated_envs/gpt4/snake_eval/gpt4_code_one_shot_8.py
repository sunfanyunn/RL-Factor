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
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])
        self.length += 1

    def get_head_position(self):
        return self.body[0]

    def self_collision(self):
        head = self.get_head_position()
        return head in self.body[1:]


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food()

    def check_collision_with_food(self):
        if self.snake.get_head_position() == (self.food.rect.x, self.food.rect.y):
            self.snake.grow()
            self.score += 1
            self.food = Food()

    def check_collision_with_boundaries(self):
        x, y = self.snake.get_head_position()
        return (x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0)

    def run(self, event):
        while not self.game_over:
            self.screen.fill((0, 0, 0))
            self.handle_events(event)
            self.snake.update()

            if self.check_collision_with_food():
                self.snake.grow()
                self.food = Food()
                self.score += 1

            if self.snake.self_collision() or self.check_collision_with_boundaries():
                self.game_over = True
                break

            self.draw_elements()
            pygame.display.update()
            self.clock.tick(10)

        return not self.game_over

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                self.snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                self.snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                self.snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                self.snake.direction = 'RIGHT'

    def draw_elements(self):
        for block in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), (block[0], block[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)
        font = pygame.font.Font(None, 36)
        text = font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(text, (5, 5))

if __name__ == '__main__':
    game = Game()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        running = game.run(event)

        if game.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render('Game Over! Score: ' + str(game.score), True, (255, 255, 255))
            game.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            text_restart = font.render('Press R to Restart or Q to Quit', True, (255, 255, 255))
            game.screen.blit(text_restart, (SCREEN_WIDTH // 2 - text_restart.get_width() // 2, SCREEN_HEIGHT // 2 - text_restart.get_height() // 2 + 50))
            pygame.display.update()

            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.reset_game()
                            waiting_for_input = False
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.QUIT:
                        waiting_for_input = False
                        pygame.quit()
                        break
