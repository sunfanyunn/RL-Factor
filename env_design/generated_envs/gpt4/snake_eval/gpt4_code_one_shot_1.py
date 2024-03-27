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

    def grow(self):
        self.length += 1
        self.body.insert(0, self.body[0])

    def update(self):
        # Get head position
        head_x, head_y = self.body[0]
        # Update body position
        if self.direction == "UP":
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == "LEFT":
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == "RIGHT":
            new_head = (head_x + GRID_SIZE, head_y)

        self.body = [new_head] + self.body[:-1]

    def change_direction(self, new_direction):
        if (self.direction, new_direction) in [("UP", "DOWN"), ("DOWN", "UP"), ("LEFT", "RIGHT"), ("RIGHT", "LEFT")]:
            return  # Ignore backward move
        self.direction = new_direction

    def head_position(self):
        return self.body[0]

    def collide_self(self):
        return self.head_position() in self.body[1:]

    def collide_walls(self):
        head_x, head_y = self.head_position()
        return head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = self.randomize_position()
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def randomize_position(self):
        return (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

    def update(self):
        self.x, self.y = self.randomize_position()
        self.rect.topleft = (self.x, self.y)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("RIGHT")

            self.snake.update()

            if self.snake.collide_self() or self.snake.collide_walls():
                self.game_over = True

            if self.snake.head_position() == (self.food.x, self.food.y):
                self.snake.grow()
                self.score += 1
                self.food.update()

            self.screen.fill(pygame.Color('black'))
            for segment in self.snake.body:
                pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.screen, pygame.Color('red'), self.food.rect)

            pygame.display.flip()
            self.clock.tick(10)

        return True  # continue running

    def display_game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render('Game Over! Score: ' + str(self.score), True, pygame.Color('white'))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        if game.game_over:
            game.display_game_over()
            game.reset_game()
        running = game.run(event)
    pygame.quit()
