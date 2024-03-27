import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_FALL_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([CATCHER_WIDTH, CATCHER_HEIGHT])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def move(self, dx):
        self.rect.x += dx
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2), -BALL_SIZE))

    def update(self):
        self.rect.y += BALL_FALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.ball_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        self.spawn_ball()

    def spawn_ball(self):
        if not self.ball_group:
            ball = Ball()
            self.ball_group.add(ball)
            self.all_sprites.add(ball)

    def run(self, event):
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.move(-10)
            if keys[pygame.K_RIGHT]:
                self.catcher.move(10)

            if pygame.sprite.spritecollide(self.catcher, self.ball_group, True):
                self.score += 1
                self.spawn_ball()

            self.all_sprites.update()

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            
            score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

        else:
            game_over_text = pygame.font.SysFont(None, 48).render('Game Over! Click to restart', True, (255, 255, 255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(60)

        for ball in self.ball_group:
            if ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                self.spawn_ball()

        return not self.game_over


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            game.run(event)
    pygame.quit()
