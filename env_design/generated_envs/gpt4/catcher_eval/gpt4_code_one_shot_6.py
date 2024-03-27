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
FONT_SIZE = 30
GAME_OVER_DELAY = 2000 # milliseconds


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def move(self, x):
        self.rect.x += x
        self.rect.x = max(0, min(SCREEN_WIDTH - CATCHER_WIDTH, self.rect.x))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(x, BALL_SIZE // 2))

    def update(self):
        self.rect.y += BALL_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = [Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE))]

    def spawn_ball(self):
        new_ball = Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE))
        self.balls.append(new_ball)

    def run(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-5)
        if keys[pygame.K_RIGHT]:
            self.catcher.move(5)

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.catcher.surf, self.catcher.rect)
        for ball in self.balls[:]:
            ball.update()
            self.screen.blit(ball.surf, ball.rect)
            if ball.rect.colliderect(self.catcher.rect):
                self.balls.remove(ball)
                self.score += 1
                self.spawn_ball()
            elif ball.rect.y > SCREEN_HEIGHT:
                self.balls.remove(ball)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                    break
                self.spawn_ball()

        score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if not self.game_over:
            lives_text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 50))
        else:
            game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(GAME_OVER_DELAY)

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
