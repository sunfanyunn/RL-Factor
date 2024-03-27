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
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - CATCHER_HEIGHT

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, SCREEN_WIDTH - CATCHER_WIDTH)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

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
        self.catcher = Catcher(SCREEN_WIDTH // 2 - CATCHER_WIDTH // 2)
        self.balls = [Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE))]

    def run(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        keys = pygame.key.get_pressed()
        self.catcher.update(keys)

        for ball in self.balls[:]:
            ball.update()
            if ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                self.balls.remove(ball)
            elif pygame.sprite.collide_rect(self.catcher, ball):
                self.score += 1
                self.balls.remove(ball)

        if not self.balls:
            self.balls.append(Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE)))

        self.screen.fill((0, 0, 0))
        for ball in self.balls:
            self.screen.blit(ball.image, ball.rect)
        self.screen.blit(self.catcher.image, self.catcher.rect)
        score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, pygame.Color('white'))
        self.screen.blit(score_text, (10, 10))

        if self.lives <= 0:
            game_over_text = pygame.font.SysFont(None, 72).render('Game Over!', True, pygame.Color('red'))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()
        self.clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
