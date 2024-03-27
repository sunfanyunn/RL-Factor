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
        self.image.fill(pygame.Color('blue'))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT / 2))

    def move(self, x_change):
        self.rect.x += x_change
        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, SCREEN_WIDTH - CATCHER_WIDTH)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(pygame.Color('red'))
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

    def add_ball(self):
        new_ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
        self.balls.append(new_ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        x_change = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x_change -= 5
        elif keys[pygame.K_RIGHT]:
            x_change += 5

        self.catcher.move(x_change)

        for ball in self.balls[:]:
            ball.update()
            if ball.rect.colliderect(self.catcher.rect):
                self.balls.remove(ball)
                self.score += 1
                self.add_ball()
            elif ball.rect.top > SCREEN_HEIGHT:
                self.balls.remove(ball)
                self.lives -= 1
                if self.lives == 0:
                    self.game_over = True
                else:
                    self.add_ball()

        self.screen.fill(pygame.Color('white'))
        self.screen.blit(self.catcher.image, self.catcher.rect)
        for ball in self.balls:
            self.screen.blit(ball.image, ball.rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', 1, pygame.Color('black'))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render('Game Over!', 1, pygame.Color('black'))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()
        self.clock.tick(60)

        return True


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
