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
        self.direction = 'RIGHT'
        self.score = 0

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
        if len(self.body) > self.score + 1:
            self.body.pop()

    def grow(self):
        self.score += 1

    def check_collisions(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)


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

    def place_food(self):
        collision = True
        while collision:
            collision = False
            self.food = Food()
            for segment in self.snake.body:
                if self.food.rect.collidepoint(segment):
                    collision = True
                    break

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        if self.snake.check_collisions():
            self.game_over = True
            return False # Stop the game loop

        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.place_food()

        self.screen.fill((0, 0, 0))

        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)
        self.display_score()
        self.clock.tick(10)
        pygame.display.flip()

        return not self.game_over

    def display_score(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Score: {self.snake.score}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def display_game_over(self):
        font = pygame.font.SysFont(None, 75)
        text = font.render('Game Over! Press R to Restart', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

if __name__ == '__main__':
    GAME = Game()
    running = True
    while running:
        if GAME.game_over:
            GAME.display_game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    GAME.reset_game()
        else:
            running = GAME.run()
    pygame.quit()

