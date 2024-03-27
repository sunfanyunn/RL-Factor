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
        self.direction = "RIGHT"
        self.length = 1

    def turn(self, direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if direction != opposite_directions[self.direction]:
            self.direction = direction

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

    def collided(self):
        head = self.body[0]
        # Check if the snake has collided with the walls
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT):
            return True
        # Check if the snake has collided with itself
        if head in self.body[1:]:
            return True
        return False


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = self.random_position()
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def random_position(self):
        return (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        self.reset_game()
        self.game_over_font = pygame.font.SysFont(None, 72)

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)
        score_text = self.font.render('Score: {}'.format(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            game_over_text = self.game_over_font.render('Game Over!', True, (255, 255, 255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            restart_text = self.font.render('Press R to Restart', True, (255, 255, 255))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
            return True

        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.turn('UP')
            elif event.key == pygame.K_DOWN:
                self.snake.turn('DOWN')
            elif event.key == pygame.K_LEFT:
                self.snake.turn('LEFT')
            elif event.key == pygame.K_RIGHT:
                self.snake.turn('RIGHT')

        self.snake.move()

        if self.snake.collided():
            self.game_over = True
        elif self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.score += 1
            self.food = Food()

        self.draw()
        pygame.display.flip()
        self.clock.tick(10)
        return True

if __name__ == "__main__":
    game = Game()

    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
