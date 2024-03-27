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
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 10))

    def move(self, direction):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= CATCHER_SPEED
        elif direction == 'right' and self.rect.right < SCREEN_WIDTH:
            self.rect.x += CATCHER_SPEED


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, BALL_COLOR, self.image.get_rect())
        self.rect = self.image.get_rect(center=(x, BALL_SIZE // 2))

    def update(self):
        self.rect.y += BALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.all_sprites = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        self.spawn_ball()

    def spawn_ball(self):
        x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        ball = Ball(x)
        self.balls.add(ball)
        self.all_sprites.add(ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move('left')
        if keys[pygame.K_RIGHT]:
            self.catcher.move('right')

        self.balls.update()

        caught_balls = pygame.sprite.spritecollide(self.catcher, self.balls, True)
        for ball in caught_balls:
            self.score += 1
            self.spawn_ball()

        for ball in self.balls:
            if ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                ball.kill()
                self.spawn_ball()
                if self.lives <= 0:
                    self.game_over = True

        self.screen.fill((0, 0, 0)) # Filling the screen with black.
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, FONT_COLOR)
        lives_text = self.font.render(f'Lives: {self.lives}', True, FONT_COLOR)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, FONT_COLOR)
            game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            self.screen.blit(game_over_text, game_over_text_rect)

        pygame.display.flip()
        self.clock.tick(60)

        if self.game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.reset_game()
            self.game_over = False

        return not self.game_over

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
