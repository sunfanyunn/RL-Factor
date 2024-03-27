import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 25
BALL_SIZE = 25
CATCHER_SPEED = 5
BALL_FALL_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(midbottom=(x, SCREEN_HEIGHT))

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-CATCHER_SPEED, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(CATCHER_SPEED, 0)

        # Keep catcher on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.surf.fill((255, 0, 0))
        x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        self.rect = self.surf.get_rect(center=(x, 0))

    def update(self):
        self.rect.move_ip(0, BALL_FALL_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        self.spawn_new_ball()

    def spawn_new_ball(self):
        new_ball = Ball()
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if self.game_over and pygame.mouse.get_pressed()[0]:
            self.reset_game()

        if not self.game_over:
            pressed_keys = pygame.key.get_pressed()
            self.catcher.update(pressed_keys)
            self.balls.update()

            for ball in pygame.sprite.spritecollide(self.catcher, self.balls, dokill=True):
                self.score += 1
                self.spawn_new_ball()

            for ball in self.balls:
                if ball.rect.bottom > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives > 0:
                        self.spawn_new_ball()

            if self.lives <= 0:
                self.game_over = True

        # Draw everything
        self.screen.fill((0, 0, 0))
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        # Draw the score
        score_surf = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surf, (5, 5))

        # Draw the lives
        lives_surf = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_surf, (5, 30))

        # Draw the game over message
        if self.game_over:
            game_over_surf = self.font.render('Game Over! Click to restart', True, (255, 255, 255))
            self.screen.blit(game_over_surf, (SCREEN_WIDTH // 2 - game_over_surf.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_surf.get_height() // 2))

        # Update the display
        pygame.display.flip()
        self.clock.tick(30)
        return True

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()
