import pygame
import sys
import random

# Define constants for the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRID_SIZE = 20

class Snake():
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.grow = False

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

        if new_head in self.body or new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT:
            return True # Collided

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        return False # Did not collide

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), (*segment, GRID_SIZE, GRID_SIZE))

    def change_direction(self, new_direction):
        # Disallow reversing the direction
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposites[self.direction]:
            self.direction = new_direction

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(self.random_position(), (GRID_SIZE, GRID_SIZE))

    def random_position(self):
        return random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE, random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def respawn(self):
        self.rect.topleft = self.random_position()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Snake Game')
        self.score_font = pygame.font.SysFont('Arial', 35)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction('RIGHT')

        if self.game_over:
            self.display_game_over()
            if pygame.key.get_pressed()[pygame.K_r]:
                self.reset_game()
            return True # continue running

        # Update
        self.game_over = self.snake.update()
        self.screen.fill((255, 255, 255))
        self.food.draw(self.screen)
        self.snake.draw(self.screen)

        if pygame.Rect(self.snake.body[0], (GRID_SIZE, GRID_SIZE)).colliderect(self.food.rect):
            self.snake.grow_snake()
            self.food.respawn()
            self.score += 1

        # Score display
        score_text = self.score_font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        # Flip the display
        pygame.display.flip()

        self.clock.tick(10 + self.score // 5) # Increase the speed based on score
        return True # continue running

    def display_game_over(self):
        game_over_text = 'Game Over! Press R to Restart'
        game_over_surface = self.score_font.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()

