import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
CATCHER_SPEED = 5
BALL_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def move(self, dx):
        self.rect.x += dx
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x=None):
        super().__init__()
        x = x if x is not None else random.randrange(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, BALL_SIZE // 2))

    def update(self):
        self.rect.y += BALL_SPEED


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        new_ball = Ball()
        self.balls.add(new_ball)

    def run(self, event):
        self.clock.tick(60)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-CATCHER_SPEED)
        elif keys[pygame.K_RIGHT]:
            self.catcher.move(CATCHER_SPEED)

        if not self.game_over:
            self.balls.update()
            for ball in self.balls:
                if ball.rect.top >= SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.spawn_ball()
                elif self.catcher.rect.colliderect(ball.rect):
                    self.score += 1
                    self.balls.remove(ball)
                    self.spawn_ball()

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.catcher.image, self.catcher.rect)
            self.balls.draw(self.screen)
            score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
            pygame.display.flip()

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            waiting = True
            while waiting:
                for evt in pygame.event.get():
                    if evt.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evt.type == pygame.MOUSEBUTTONDOWN or (evt.type == pygame.KEYDOWN and evt.key == pygame.K_RETURN):
                        waiting = False
                        self.reset_game()

        return not self.game_over


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
