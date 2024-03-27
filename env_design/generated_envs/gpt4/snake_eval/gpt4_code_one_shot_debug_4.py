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
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self, food_pos):
        head_x, head_y = self.body[0]
        if (head_x < 0 or head_x >= SCREEN_WIDTH or
                head_y < 0 or head_y >= SCREEN_HEIGHT):
            return 'collision'
        if len(self.body) != len(set(self.body)):
            return 'collision'
        if (head_x, head_y) == food_pos:
            return 'ate_food'
        return 'none'

    def change_direction(self, new_dir):
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_dir not in opposites or new_dir != opposites[self.direction]:
            self.direction = new_dir


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption('Snake Game')
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.food = Food()

    def run(self, event):
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

        self.snake.move()
        collision_status = self.snake.check_collision((self.food.x, self.food.y))
        if collision_status == 'collision':
            self.game_over = True
        elif collision_status == 'ate_food':
            self.snake.grow()
            self.score += 1
            self.food = Food()

        self.screen.fill((0, 0, 0))
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food.x, self.food.y, GRID_SIZE, GRID_SIZE))
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))
        pygame.display.flip()
        self.clock.tick(10)

        if self.game_over:
            self.show_game_over()

        return not self.game_over

    def show_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        score_text = self.font.render(f'Final Score: {self.score}', True, (255, 255, 255))
        restart_text = self.font.render('Press R to Restart', True, (255, 255, 255))

        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
        self.screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
        pygame.display.flip()

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting_for_restart = False
                    self.reset_game()
                    break
        return True


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type != pygame.NOEVENT:
            running = game.run(event)
    pygame.quit()
