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
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 10


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2), 0))

    def update(self):
        self.rect.y += BALL_FALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont(None, 36)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.balls.add(Ball())

    def run(self):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        keys = pygame.key.get_pressed()
        self.catcher.update(keys)
        self.balls.update()

        for ball in list(self.balls):
            if ball.rect.top > SCREEN_HEIGHT:
                self.balls.remove(ball)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                    break
                else:
                    self.balls.add(Ball())
            elif pygame.sprite.collide_rect(self.catcher, ball):
                self.score += 1
                self.balls.remove(ball)
                self.balls.add(Ball())

        self.screen.fill((0, 0, 0))
        self.balls.draw(self.screen)
        self.screen.blit(self.catcher.image, self.catcher.rect)

        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.lives <= 0:
            game_over_text = self.font.render('Game Over! Click to continue...', True, (255, 255, 255))
            self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        self.clock.tick(30)
        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run()
    pygame.quit()
