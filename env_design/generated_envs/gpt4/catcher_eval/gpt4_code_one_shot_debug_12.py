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
    def __init__(self, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - CATCHER_HEIGHT):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, SCREEN_WIDTH - CATCHER_WIDTH)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x=random.randint(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, BALL_SIZE // 2))

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
        self.catcher = Catcher()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        new_ball = Ball()
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    self.reset_game()

            keys = pygame.key.get_pressed()
            self.catcher.update(keys)
            self.balls.update()

            hit_balls = pygame.sprite.spritecollide(self.catcher, self.balls, True)
            for ball in hit_balls:
                self.score += 1
                self.spawn_ball()

            for ball in list(self.balls):
                if ball.rect.bottom > SCREEN_HEIGHT:
                    self.lives -= 1
                    self.spawn_ball()
                    if self.lives <= 0:
                        self.game_over = True
                    ball.kill()

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)

            score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, pygame.Color('white'))
            self.screen.blit(score_text, (10, 10))

            if self.game_over:
                game_over_text = pygame.font.SysFont(None, 72).render('Game Over!', True, pygame.Color('red'))
                self.screen.blit(game_over_text, (
                    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

            pygame.display.flip()
            self.clock.tick(30)

        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
