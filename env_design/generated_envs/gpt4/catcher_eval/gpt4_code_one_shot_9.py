import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_DIAMETER = 20
BALL_RADIUS = BALL_DIAMETER // 2

class Catcher(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, x):
        self.rect.x = x

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)


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
        self.catcher = Catcher(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, CATCHER_WIDTH, CATCHER_HEIGHT)
        self.balls = [Ball(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS), -BALL_RADIUS, BALL_RADIUS)]

    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.update(max(0, self.catcher.rect.x - 5))
            if keys[pygame.K_RIGHT]:
                self.catcher.update(min(SCREEN_WIDTH - CATCHER_WIDTH, self.catcher.rect.x + 5))

            if len(self.balls) < 1:
                self.balls.append(Ball(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS), -BALL_RADIUS, BALL_RADIUS))

            self.screen.fill((0, 0, 0))
            for ball in self.balls:
                ball.update()
                if self.catcher.rect.colliderect(ball.rect):
                    self.score += 1
                    self.balls.remove(ball)
                elif ball.rect.y > SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                    if self.lives <= 0:
                        self.game_over = True

            for ball in self.balls:
                ball.draw(self.screen)
            self.catcher.draw(self.screen)

            score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
            lives_text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))

            if self.game_over:
                game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                self.reset_game()

            pygame.display.flip()
            self.clock.tick(60)

        return True

if __name__ == "__main__":
    game = Game()
    running = game.run(None)
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
