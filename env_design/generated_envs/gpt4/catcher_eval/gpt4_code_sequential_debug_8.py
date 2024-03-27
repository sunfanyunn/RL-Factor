import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 150
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_FALL_SPEED = 5
BALL_SPAWN_RATE = 1000  # milliseconds
FONT_SIZE = 30
GAME_FONT = 'Arial'


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 30))

    def move(self, x_change):
        self.rect.x += x_change
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midtop=(x, 0))

    def update(self):
        self.rect.y += BALL_FALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(GAME_FONT, FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.catcher_sprite = pygame.sprite.Group(self.catcher)
        pygame.time.set_timer(pygame.USEREVENT + 1, BALL_SPAWN_RATE)

    def spawn_ball(self):
        x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
        ball = Ball(x)
        self.balls.add(ball)

    def run(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.USEREVENT + 1:
                self.spawn_ball()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-10)
        if keys[pygame.K_RIGHT]:
            self.catcher.move(10)

        self.balls.update()
        self.screen.fill((0, 0, 0))
        self.balls.draw(self.screen)
        self.catcher_sprite.draw(self.screen)

        self.score_display = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(self.score_display, (10, 10))

        if pygame.sprite.spritecollide(self.catcher, self.balls, True):
            self.score += 1

        for ball in list(self.balls):
            if ball.rect.top > SCREEN_HEIGHT:
                self.balls.remove(ball)
                self.lives -= 1
                if self.lives == 0:
                    self.game_over = True

        self.lives_display = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(self.lives_display, (SCREEN_WIDTH - 100, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        self.clock.tick(60)
        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
