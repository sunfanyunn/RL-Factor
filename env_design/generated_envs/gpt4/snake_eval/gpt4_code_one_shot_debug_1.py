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

    def grow(self):
        self.length += 1

    def update(self, new_direction=None):
        if new_direction:
            if (new_direction == 'UP' and self.direction != 'DOWN') or \
               (new_direction == 'DOWN' and self.direction != 'UP') or \
               (new_direction == 'LEFT' and self.direction != 'RIGHT') or \
               (new_direction == 'RIGHT' and self.direction != 'LEFT'):
                self.direction = new_direction
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

    def render(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def collides_with_bounds(self):
        x, y = self.body[0]
        return x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = Food.randomized_position()

    @staticmethod
    def randomized_position():
        return (random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))


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
        self.score = 0

    def run(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.update('UP')
            elif event.key == pygame.K_DOWN:
                self.snake.update('DOWN')
            elif event.key == pygame.K_LEFT:
                self.snake.update('LEFT')
            elif event.key == pygame.K_RIGHT:
                self.snake.update('RIGHT')

        if not self.game_over:
            self.snake.update()
            if self.snake.collides_with_self() or self.snake.collides_with_bounds():
                self.game_over = True
            elif self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.food = Food()
                self.score += 1

        self.screen.fill((0, 0, 0))
        self.snake.render(self.screen)
        self.food.render(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.display_game_over()
        pygame.display.flip()
        self.clock.tick(10)
        return not self.game_over

    def display_game_over(self):
        game_over_text = self.font.render('Game Over! Press R to Restart or Q to Quit', True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(game_over_text, game_over_rect)


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game.game_over:
            game.reset_game()
            game.game_over = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q and game.game_over:
            running = False
        else:
            running = game.run(event)
    pygame.quit()
