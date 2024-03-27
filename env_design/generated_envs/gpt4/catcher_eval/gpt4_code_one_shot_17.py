import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5
CATCHER_SPEED = 10


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def update(self, x):
        self.rect.x = x
        self.rect.clamp_ip(self.rect.clamp(self.image.get_rect()))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.filleshoot((255, 0, 0))
        self.rect = self.image.get_rect(midtop=(x, 0))

    def update(self):
        self.rect.y += BALL_SPEED


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
        self.balls = [Ball(random.randint(0, SCREEN_WIDTH))]  # Ensures initial non-empty list

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.update(max(0, self.catcher.rect.x - CATCHER_SPEED))
        if keys[pygame.K_RIGHT]:
            self.catcher.update(min(SCREEN_WIDTH - CATCHER_WIDTH, self.catcher.rect.x + CATCHER_SPEED))

        if not self.balls:
            self.balls.append(Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE)))

        for ball in self.balls[:]:
            ball.update()
            if ball.rect.colliderect(self.catcher.rect):
                self.score += 1
                self.balls.remove(ball)
            elif ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                self.balls.remove(ball)
                if self.lives == 0:
                    self.game_over = True

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.catcher.image, self.catcher.rect)
        for ball in self.balls:
            self.screen.blit(ball.image, ball.rect)
        pygame.display.flip()
        self.clock.tick(60)
        return True

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Catcher Game')
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
