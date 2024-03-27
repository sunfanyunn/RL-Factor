import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
CATCHER_COLOR = (255, 255, 255)
BALL_COLOR = (255, 0, 0)
BALL_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(CATCHER_COLOR)
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT))

    def update(self, direction):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= 10
        elif direction == 'right' and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 10


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect(center=(x, 0))

    def update(self):
        self.rect.y += BALL_SPEED
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
        self.catcher_group = pygame.sprite.Group(self.catcher)
        self.ball_group = pygame.sprite.Group()

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.update('left')
            if keys[pygame.K_RIGHT]:
                self.catcher.update('right')

            if len(self.ball_group) == 0 or random.randint(0, 50) == 0:
                new_ball = Ball(random.randint(0, SCREEN_WIDTH))
                self.ball_group.add(new_ball)

            self.ball_group.update()

            collisions = pygame.sprite.spritecollide(self.catcher, self.ball_group, True)
            self.score += len(collisions)

            for ball in self.ball_group:
                if ball.rect.bottom >= SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives == 0:
                        self.game_over = True

            self.screen.fill((0, 0, 0))
            self.catcher_group.draw(self.screen)
            self.ball_group.draw(self.screen)

            score_text = f'Score: {self.score} Lives: {self.lives}'
            score_surface = pygame.font.Font(None, 36).render(score_text, True, (255, 255, 255))
            self.screen.blit(score_surface, (10, 10))

            if self.game_over:
                game_over_surface = pygame.font.Font(None, 72).render('Game Over!', True, (255, 0, 0))
                game_over_rect = game_over_surface.get_rect(center=self.screen.get_rect().center)
                self.screen.blit(game_over_surface, game_over_rect)

            pygame.display.flip()
            self.clock.tick(60)

        while self.game_over:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.reset_game()
                break

        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
