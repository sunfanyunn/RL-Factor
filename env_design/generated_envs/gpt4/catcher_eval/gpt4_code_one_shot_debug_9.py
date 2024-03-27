import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_DIAMETER = 20
BALL_RADIUS = BALL_DIAMETER // 2


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([CATCHER_WIDTH, CATCHER_HEIGHT])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 10))

    def move(self, x):
        new_x = self.rect.x + x
        if 0 <= new_x <= SCREEN_WIDTH - CATCHER_WIDTH:
            self.rect.x = new_x


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_DIAMETER, BALL_DIAMETER], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS), 0))
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.balls.add(Ball())
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0

    def run(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-5)
        if keys[pygame.K_RIGHT]:
            self.catcher.move(5)

        if len(self.balls) == 0:
            self.balls.add(Ball())

        if not self.game_over:
            self.balls.update()
            collisions = pygame.sprite.spritecollide(self.catcher, self.balls, True)
            self.score += len(collisions)

        for ball in list(self.balls):
            if ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                ball.kill()
                if self.lives <= 0:
                    self.game_over = True

        self.screen.fill((0, 0, 0))
        if self.game_over:
            game_over_text = self.font.render('Game Over! Click to Continue.', True, (255, 255, 255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        else:
            self.balls.draw(self.screen)
            self.screen.blit(self.catcher.image, self.catcher.rect)
            score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))

        pygame.display.flip()
        self.clock.tick(60)

    def check_reset_game(self):
        mouse_pressed = pygame.mouse.get_pressed()
        if self.game_over and mouse_pressed[0]:
            self.reset_game()

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.run(event)
        game.check_reset_game()
    pygame.quit()
