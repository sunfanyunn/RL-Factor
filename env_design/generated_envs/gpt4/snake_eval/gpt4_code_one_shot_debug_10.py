import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
# Define the size of each grid unit / snake's body segment
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

    def change_direction(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE
        self.y = random.randint(0, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def respawn(self):
        self.x = random.randint(0, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE
        self.y = random.randint(0, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE
        self.rect.topleft = (self.x, self.y)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction('RIGHT')
                elif event.key == pygame.K_r:
                    self.reset_game()

        self.screen.fill((0, 0, 0))
        if not self.game_over:
            self.snake.update()
            if self.snake.body[0] == (self.food.x, self.food.y):
                self.score += 1
                self.snake.grow()
                self.food.respawn()

            for segment in self.snake.body:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))

            pygame.draw.rect(self.screen, (255, 0, 0), self.food.rect)

            score_text = self.font.render('Score: {}'.format(self.score), True, (255, 255, 255))
            self.screen.blit(score_text, (5, 5))

            self.game_over = self.check_collisions()

            if self.game_over:
                self.show_game_over()

        pygame.display.flip()
        self.clock.tick(10)
        return not self.game_over

    def check_collisions(self):
        head_x, head_y = self.snake.body[0]
        if head_x < 0 or head_y < 0 or head_x >= SCREEN_WIDTH or head_y >= SCREEN_HEIGHT or self.snake.body[0] in self.snake.body[1:]:
            return True
        return False

    def show_game_over(self):
        game_over_text = self.font.render('GAME OVER! Press R to restart.', True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(5000)

        # Wait for the R key to restart
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting_for_key = False

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
