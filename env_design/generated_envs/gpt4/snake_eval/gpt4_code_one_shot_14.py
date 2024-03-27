import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = "RIGHT"
        self.length = 1

    def update(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            head_y -= GRID_SIZE
        elif self.direction == "DOWN":
            head_y += GRID_SIZE
        elif self.direction == "LEFT":
            head_x -= GRID_SIZE
        elif self.direction == "RIGHT":
            head_x += GRID_SIZE
        new_head = (head_x, head_y)
        if (head_x < 0 or head_y < 0 or head_x >= SCREEN_WIDTH or head_y >= SCREEN_HEIGHT or new_head in self.body):
            raise ValueError('Game over')

        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def change_direction(self, new_direction):
        """Change the snake's direction without allowing it to go back on itself."""
        opposite_directions = {('UP', 'DOWN'), ('LEFT', 'RIGHT')}
        if (self.direction, new_direction) not in opposite_directions:
            self.direction = new_direction


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("red"), self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self, event):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN and not self.game_over:
                if e.key == pygame.K_UP:
                    self.snake.change_direction('UP')
                elif e.key == pygame.K_DOWN:
                    self.snake.change_direction('DOWN')
                elif e.key == pygame.K_LEFT:
                    self.snake.change_direction('LEFT')
                elif e.key == pygame.K_RIGHT:
                    self.snake.change_direction('RIGHT')

        try:
            if not self.game_over:
                self.snake.update()
            if self.snake.body[0] == (self.food.x, self.food.y):
                self.snake.grow()
                self.score += 10
                self.food = Food()
        except ValueError:
            self.game_over = True

        self.screen.fill(pygame.Color("black"))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, pygame.Color("green"), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        self.food.draw(self.screen)

        if self.game_over:
            font = pygame.font.Font(None, 74)
            text = font.render('Game Over!', 1, (255, 0, 0))
            self.screen.blit(text, ((SCREEN_WIDTH // 2) - text.get_width() // 2, SCREEN_HEIGHT // 2))
            font = pygame.font.Font(None, 36)
            restart_text = font.render('Press R to Restart', 1, (255, 255, 255))
            self.screen.blit(restart_text, ((SCREEN_WIDTH // 2) - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

        font = pygame.font.Font(None, 36)
        score_text = font.render('Score: ' + str(self.score), 1, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))

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
