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
        self.body = [((SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE, (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE)]
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
        self.body.insert(0, (head_x, head_y))
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def check_collision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True
        for segment in self.body[1:]:
            if segment == (head_x, head_y):
                return True
        return False

    def change_direction(self, new_direction):
        """Change direction of the snake if not directly backward."""
        if (new_direction == 'UP' and not self.direction == 'DOWN') or\
           (new_direction == 'DOWN' and not self.direction == 'UP') or\
           (new_direction == 'LEFT' and not self.direction == 'RIGHT') or\
           (new_direction == 'RIGHT' and not self.direction == 'LEFT'):
            self.direction = new_direction


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def redraw(self):
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def draw_objects(self):
        self.screen.fill(pygame.Color('black'))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, pygame.Color('red'), self.food.rect)
        score_text = self.font.render(f'Score: {self.score}', True, pygame.Color('white'))
        self.screen.blit(score_text, (10, 10))

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.change_direction('UP')
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction('DOWN')
            elif event.key == pygame.K_LEFT:
                self.snake.change_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction('RIGHT')
        return True

    def run(self, event):
        if self.handle_events(event) == False:
            return False
        if not self.game_over:
            self.snake.update()
            if self.snake.check_collision():
                self.game_over = True
                game_over_text = self.font.render('Game Over! Press R to Restart or Q to Quit', True, pygame.Color('white'))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
                pygame.display.flip()
            elif (self.snake.body[0][0] == self.food.x) and (self.snake.body[0][1] == self.food.y):
                self.snake.grow()
                self.food.redraw()
                self.score += 1
            self.draw_objects()
            pygame.display.flip()
            self.clock.tick(10)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    return False
        return True

if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
