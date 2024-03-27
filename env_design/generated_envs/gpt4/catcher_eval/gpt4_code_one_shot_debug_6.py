import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5
FONT_SIZE = 30
GAME_OVER_DELAY = 2000 # milliseconds

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=(x, SCREEN_HEIGHT - 30))

    def move(self, x):
        self.rect.x += x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, RED, (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect = self.surf.get_rect(center=(x, 0))

    def update(self):
        self.rect.y += BALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.ball_group = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        new_ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
        self.ball_group.add(new_ball)

    def run(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-5)
        if keys[pygame.K_RIGHT]:
            self.catcher.move(5)

        self.screen.fill(BLACK)
        self.screen.blit(self.catcher.surf, self.catcher.rect)

        for ball in self.ball_group:
            ball.update()
            self.screen.blit(ball.surf, ball.rect)
            if pygame.sprite.collide_rect(self.catcher, ball):
                self.score += 1
                ball.kill()
                self.spawn_ball()
            elif ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                ball.kill()
                self.spawn_ball()
                if self.lives <= 0:
                    self.game_over = True
                    pygame.time.set_timer(pygame.USEREVENT, GAME_OVER_DELAY)

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        lives_text = self.font.render(f'Lives: {self.lives}', True, WHITE)
        self.screen.blit(lives_text, (10, 45))

        if self.game_over:
            game_over_text = self.font.render('Game Over! Click to continue', True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()
        self.clock.tick(60)

        return True


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                game.game_over = False
                pygame.time.set_timer(pygame.USEREVENT, 0) # Turn off the timer
            else:
                running = game.run(event)
    pygame.quit()
