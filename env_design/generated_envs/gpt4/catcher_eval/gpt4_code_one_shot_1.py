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
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midtop=(x, 0))

    def update(self):
        self.rect.y += BALL_FALL_SPEED
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.display.set_caption('Catcher Game')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.balls.add(Ball(random.randint(0, SCREEN_WIDTH)))
        self.catcher_group = pygame.sprite.Group(self.catcher)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    self.reset_game()

            keys = pygame.key.get_pressed()
            self.catcher.update(keys)

            if not self.game_over:
                self.balls.update()

                hit = pygame.sprite.groupcollide(self.balls, self.catcher_group, True, False)
                if hit:
                    self.score += len(hit)
                    self.balls.add(Ball(random.randint(0, SCREEN_WIDTH)))

                for ball in self.balls:
                    if ball.rect.bottom >= SCREEN_HEIGHT:
                        self.lives -= 1
                        ball.kill()
                        if self.lives > 0:
                            self.balls.add(Ball(random.randint(0, SCREEN_WIDTH)))
                        else:
                            self.game_over = True

            self.screen.fill((0, 0, 0))
            self.balls.draw(self.screen)
            self.catcher_group.draw(self.screen)
            score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            if self.game_over:
                game_over_text = self.font.render('Game Over! Click to restart.', True, (255, 255, 255))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

            pygame.display.flip()
            self.clock.tick(30)
        return True


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = game.run()
    pygame.quit()