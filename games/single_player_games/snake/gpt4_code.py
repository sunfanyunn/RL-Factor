import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 60, 100, 50)
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def update_game_state(self):
        if not self.game_over:
            self.snake.update()
            if self.snake.check_collision():
                self.game_over = True
            elif self.snake.eat_food(self.food):
                self.score += 1
                self.food.randomize_position()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                ]:
                    self.snake.change_direction(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.collidepoint(event.pos):
                    self.reset_game()

    def run(self):
        while True:
            self.handle_events()
            self.update_game_state()
            self.render_game()
            self.clock.tick(FPS)

    def render_game(self):
        self.screen.fill(GREEN)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        pygame.draw.rect(self.screen, BLACK, self.reset_button, 2)
        reset_text = self.font.render("Reset", True, BLACK)
        self.screen.blit(reset_text, (WIDTH // 2 - 30, HEIGHT - 50))
        pygame.display.flip()


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = pygame.K_UP
        self.new_direction = self.direction

    def update(self):
        if self.new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.direction = self.new_direction
        elif self.new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.direction = self.new_direction
        elif self.new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.direction = self.new_direction
        elif self.new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.direction = self.new_direction

        if self.direction == pygame.K_UP:
            new_head = (self.body[0][0], self.body[0][1] - 1)
        elif self.direction == pygame.K_DOWN:
            new_head = (self.body[0][0], self.body[0][1] + 1)
        elif self.direction == pygame.K_LEFT:
            new_head = (self.body[0][0] - 1, self.body[0][1])
        elif self.direction == pygame.K_RIGHT:
            new_head = (self.body[0][0] + 1, self.body[0][1])

        self.body.insert(0, new_head)
        self.body.pop()

    def change_direction(self, new_direction):
        self.new_direction = new_direction

    def check_collision(self):
        return (
            (self.body[0] in self.body[1:])
            or (self.body[0][0] < 0 or self.body[0][0] >= GRID_WIDTH)
            or (self.body[0][1] < 0 or self.body[0][1] >= GRID_HEIGHT)
        )

    def eat_food(self, food):
        if self.body[0] == (food.rect.x // GRID_SIZE, food.rect.y // GRID_SIZE):
            self.body.append(self.body[-1])
            return True
        return False

    def draw(self, surface):
        for part in self.body:
            pygame.draw.rect(
                surface,
                BLACK,
                pygame.Rect(
                    part[0] * GRID_SIZE, part[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
                ),
            )


class Food:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE)
        self.randomize_position()

    def randomize_position(self):
        self.rect.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
