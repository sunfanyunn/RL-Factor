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
        self.direction = "RIGHT"
        self.length = 1

    def move(self):
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
        # Add new position of the head
        self.body.insert(0, new_head)
        # Remove the last segment of the snake's body
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def check_collision(self):
        x, y = self.body[0]
        # Check if the snake has collided with the walls:
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return True
        # Check if the snake has collided with itself:
        if (x, y) in self.body[1:]:
            return True
        return False

    def change_direction(self, new_dir):
        """Change the direction of the snake, not allowing it to move backward."""
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if opposite_directions[new_dir] != self.direction:
            self.direction = new_dir


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = self.random_position()

    def random_position(self):
        return (random.randint(0, (SCREEN_WIDTH-GRID_SIZE)//GRID_SIZE)*GRID_SIZE, 
                random.randint(0, (SCREEN_HEIGHT-GRID_SIZE)//GRID_SIZE)*GRID_SIZE)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
        if self.game_over:
            self.show_game_over()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
            return True

        self.handle_events(event)
        self.snake.move()

        if self.snake.check_collision():
            self.game_over = True

        # Check if the snake eats the food
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.grow()
            self.score += 1
            self.food = Food()

        self.update_screen()
        self.clock.tick(10)
        return not self.game_over

    def update_screen(self):
        self.screen.fill((0, 0, 0))

        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        pygame.draw.rect(self.screen, (255, 0, 0), (self.food.x, self.food.y, GRID_SIZE, GRID_SIZE))

        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))

        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.change_direction('UP')
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction('DOWN')
            elif event.key == pygame.K_LEFT:
                self.snake.change_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction('RIGHT')

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        score_text = self.font.render(f'Final Score: {self.score}', True, (255, 255, 255))
        restart_text = self.font.render('Press R to Restart', True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
    pygame.quit()
