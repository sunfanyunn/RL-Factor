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
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT / 2))

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, SCREEN_WIDTH - CATCHER_WIDTH)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, BALL_SIZE / 2))

    def update(self):
        self.rect.y += BALL_FALL_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = [Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))]

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.move(-10)
            if keys[pygame.K_RIGHT]:
                self.catcher.move(10)

            self.screen.fill((0, 0, 0))

            for ball in self.balls:
                ball.update()
                self.screen.blit(ball.image, ball.rect)
                if ball.rect.y >= SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                if pygame.sprite.collide_rect(self.catcher, ball):
                    self.score += 1
                    self.balls.remove(ball)

            if len(self.balls) == 0:
                new_ball_x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
                self.balls.append(Ball(new_ball_x))

            self.screen.blit(self.catcher.image, self.catcher.rect)
            score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            if self.lives <= 0:
                self.game_over = True
                game_over_text = pygame.font.SysFont(None, 48).render('Game Over! Click to restart', True, (255, 255, 255))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        else:
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
