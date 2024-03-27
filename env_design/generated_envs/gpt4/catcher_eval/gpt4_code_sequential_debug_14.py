import pygame
import sys
import random

# Initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 150
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5

# Initialize Pygame
pygame.init()

class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 30))

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 10

class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect(center=(x, BALL_SIZE // 2))

    def update(self):
        self.rect.y += BALL_SPEED

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        self.ball_spawn_timer = pygame.time.get_ticks()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.spawn_ball()
        self.ball_spawn_timer = pygame.time.get_ticks()

    def spawn_ball(self):
        x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        ball = Ball(x)
        self.balls.add(ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        current_time = pygame.time.get_ticks()
        if not self.game_over:
            keys = pygame.key.get_pressed()
            self.catcher.update(keys)
            self.balls.update()

            if current_time - self.ball_spawn_timer > 2000 or len(self.balls) == 0:
                self.spawn_ball()
                self.ball_spawn_timer = current_time

            # Collision detection
            hit_list = pygame.sprite.spritecollide(self.catcher, self.balls, True)
            for ball in hit_list:
                self.score += 1
                global BALL_SPEED
                BALL_SPEED += 0.1 * self.score
                if self.catcher.rect.width > 50:
                    CATCHER_WIDTH = max(50, self.catcher.rect.width - 0.1 * self.score)
                    self.catcher.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
                    self.catcher.image.fill((0, 255, 0))
                    self.catcher.rect.width = CATCHER_WIDTH
                self.spawn_ball()

            # Check for missed balls
            for ball in self.balls:
                if ball.rect.top > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives > 0:
                        self.spawn_ball()
                    else:
                        self.game_over = True
                        break
            self.screen.fill((0, 0, 0))  # Fill screen with black
            self.balls.draw(self.screen)
            self.screen.blit(self.catcher.image, self.catcher.rect)
            self.display_score()
            self.display_lives()
        else:
            self.display_game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))

    def display_lives(self):
        lives_surf = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_surf, (SCREEN_WIDTH - 110, 10))

    def display_game_over(self):
        game_over_surf = self.font.render('Game Over!', True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surf, game_over_rect)

        restart_surf = self.font.render('Click to restart', True, (255, 255, 255))
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_surf, restart_rect)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
    pygame.quit()

