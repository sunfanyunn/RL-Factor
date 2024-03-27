import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_COLOR = (255, 255, 255) # White
BALL_COLOR = (255, 0, 0) # Red
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5
CATCHER_SPEED = 10
CATCHER_WIDTH = 100
FONT_COLOR = (0, 0, 0) # Black


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(CATCHER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - CATCHER_HEIGHT

    def move(self, direction):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= CATCHER_SPEED
        elif direction == 'right' and self.rect.right < SCREEN_WIDTH:
            self.rect.x += CATCHER_SPEED


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

    def update(self):
        self.rect.y += BALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2 - CATCHER_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
        ball = Ball(x)
        self.balls.add(ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.move('left')
            if keys[pygame.K_RIGHT]:
                self.catcher.move('right')
            self.balls.update()
            self.screen.fill((0, 0, 0)) # Filling the screen with black.
            self.balls.draw(self.screen)
            self.screen.blit(self.catcher.image, self.catcher.rect)
            score_text = self.font.render(f'Score: {self.score}', True, FONT_COLOR)
            lives_text = self.font.render(f'Lives: {self.lives}', True, FONT_COLOR)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            # Collision detection
            caught_balls = pygame.sprite.spritecollide(self.catcher, self.balls, True)
            for ball in caught_balls:
                self.score += 1
                self.spawn_ball()
            # Check for missed balls
            for ball in self.balls:
                if ball.rect.top > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives > 0:
                        self.spawn_ball()
            if self.lives <= 0:
                self.game_over = True
        else:
            game_over_text = self.font.render('Game Over!', True, FONT_COLOR)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
        pygame.display.flip()
        self.clock.tick(60)
        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
