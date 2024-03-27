import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_FALL_SPEED = 5
CATCHER_MOVE_SPEED = 5
FONT_SIZE = 30
GAME_OVER_FONT_SIZE = 90
RESTART_TEXT_SIZE = 50


# define a main class named 'Catcher' which represents the player
# define another class named 'Ball' which represents the falling balls
# define another class named 'Game' which handles the game logic and display

class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([CATCHER_WIDTH, CATCHER_HEIGHT])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 30))

    def move(self, delta_x):
        self.rect.x += delta_x * CATCHER_MOVE_SPEED
        self.rect.x = max(0, min(SCREEN_WIDTH - CATCHER_WIDTH, self.rect.x))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, BALL_SIZE // 2))

    def update(self):
        self.rect.y += BALL_FALL_SPEED
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()
            global missed_ball
            missed_ball = True


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.game_over_font = pygame.font.SysFont(None, GAME_OVER_FONT_SIZE)
        self.restart_font = pygame.font.SysFont(None, RESTART_TEXT_SIZE)
        self.reset_game()
        global missed_ball
        missed_ball = False

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.balls.add(Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)))

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.catcher.move(-1)
            elif event.key == pygame.K_RIGHT:
                self.catcher.move(1)
            elif event.key == pygame.K_r and self.game_over:
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:  # Allow pressing ESC to quit
                return False
        elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:  # Handle MOUSEBUTTONDOWN for restart
            x, y = pygame.mouse.get_pos()
            # Restart game if within restart rect
            if restart_rect.collidepoint(x, y):
                self.reset_game()

        if not self.game_over:
            self.update_game()
        self.draw_game()
        pygame.display.flip()
        self.clock.tick(60)
        return True

    def update_game(self):
        self.balls.update()

        # Check collision
        for ball in self.balls:
            if pygame.sprite.collide_rect(self.catcher, ball):
                self.score += 1
                ball.kill()

        # Add new balls
        if len(self.balls) == 0 or self.balls.sprites()[-1].rect.y > BALL_SIZE * 2:
            x_position = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
            self.balls.add(Ball(x_position))

        # Check if ball hits bottom and reduce lives
        global missed_ball
        if missed_ball:
            self.lives -= 1
            missed_ball = False
            if self.lives <= 0:
                self.game_over = True
            else:
                self.balls.add(Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)))

    def draw_game(self):
        self.screen.fill((0, 0, 0))
        self.balls.draw(self.screen)
        self.screen.blit(self.catcher.image, self.catcher.rect)
        self.show_score()
        self.show_lives()  # Call to new show_lives method

        if self.game_over:
            global restart_rect
            restart_rect = self.show_game_over()

    def show_score(self):
        score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(topleft=(10, 10))
        self.screen.blit(score_surface, score_rect)

    # New method to display remaining lives
    def show_lives(self):
        lives_surface = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        lives_rect = lives_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(lives_surface, lives_rect)

    def show_game_over(self):
        game_over_surface = self.game_over_font.render('Game Over!', True, (255, 255, 255))
        restart_surface = self.restart_font.render('Click to Restart', True, (255, 255, 255))  # Change text to 'Click to Restart'
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - GAME_OVER_FONT_SIZE // 4))
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + RESTART_TEXT_SIZE // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        self.screen.blit(restart_surface, restart_rect)
        return restart_rect  # Return the rect for restart text

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()



