import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_SIZE = (100, 20)
BALL_SIZE = (20, 20)
BALL_DROP_SPEED = 5
CATCHER_SPEED = 10
BALL_SPAWN_RATE = 30
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 74
DIFFICULTY_INCREASE_RATE = 5

# Initialize Pygame
pygame.init()

class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface(CATCHER_SIZE)
        self.image.fill(TEXT_COLOR)
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT))

    def update(self, dx=0):
        self.rect.x += dx * CATCHER_SPEED
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(BALL_SIZE)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))

    def update(self):
        self.rect.y += BALL_DROP_SPEED

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher_group = pygame.sprite.GroupSingle(Catcher(SCREEN_WIDTH // 2))
        self.ball_group = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        if len(self.ball_group.sprites()) < 1:
            self.ball_group.add(Ball())

    def run(self, event):
        running = True
        self.clock.tick(60)

        if not self.game_over:
            keys = pygame.key.get_pressed()
            dx = 0
            if keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_RIGHT]:
                dx += 1
            self.catcher_group.update(dx)

            self.ball_group.update()
            collisions = pygame.sprite.spritecollide(self.catcher_group.sprite, self.ball_group, dokill=True)
            self.score += len(collisions)

            # Increase difficulty based on score
            if self.score % DIFFICULTY_INCREASE_RATE == 0 and len(collisions) > 0:
                global BALL_DROP_SPEED
                BALL_DROP_SPEED += 1 # Increase ball drop speed
                # Optionally, you can also decrease the catcher size and adjust its position

            for ball in list(self.ball_group):
                if ball.rect.bottom >= SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()

            self.spawn_ball()

            if self.lives <= 0:
                self.game_over = True

            self.screen.fill((0, 0, 0))
            self.catcher_group.draw(self.screen)
            self.ball_group.draw(self.screen)
            self.display_score()
            self.display_lives()
            pygame.display.flip()

        else:
            self.display_game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
                return True

        return running

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))

    def display_lives(self):
        lives_text = self.font.render(f'Lives: {self.lives}', True, TEXT_COLOR)
        self.screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

    def display_game_over(self):
        game_over_text = self.font.render('Game Over! Click to continue', True, TEXT_COLOR)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    frame_count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            running = game.run(event)
        if frame_count % BALL_SPAWN_RATE == 0:
            game.spawn_ball()
        frame_count += 1
    pygame.quit()

