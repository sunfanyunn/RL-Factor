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
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, SCREEN_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, SCREEN_WIDTH - CATCHER_WIDTH)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, 0)

    def update(self):
        self.rect.y += BALL_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        mid_x = SCREEN_WIDTH // 2
        self.catcher = Catcher(mid_x)
        self.balls = [Ball(random.randint(0, SCREEN_WIDTH))]

    def spawn_ball(self):
        new_ball = Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE))
        self.balls.append(new_ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-CATCHER_SPEED)
        elif keys[pygame.K_RIGHT]:
            self.catcher.move(CATCHER_SPEED)

        if not self.game_over:
            for ball in self.balls:
                ball.update()
                if ball.rect.top > SCREEN_HEIGHT:
                    self.balls.remove(ball)
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over = True
                        break
                    self.spawn_ball()
                if self.catcher.rect.colliderect(ball.rect):
                    self.balls.remove(ball)
                    self.score += 1
                    self.spawn_ball()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.catcher.image, self.catcher.rect)
            for ball in self.balls:
                self.screen.blit(ball.image, ball.rect)
            score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            if self.game_over:
                game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
                self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
                pygame.display.flip()
                pygame.time.wait(3000)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.reset_game()
        pygame.display.flip()
        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
