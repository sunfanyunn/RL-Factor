import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_DIAMETER = 20
BALL_RADIUS = BALL_DIAMETER // 2


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))  # White catcher
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT))

    def move(self, move_x):
        self.rect.x += move_x
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))  # Prevents moving beyond the screen


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_DIAMETER, BALL_DIAMETER), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)  # Red ball
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.balls.add(Ball(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)))

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.reset_game()

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.move(-5)
            if keys[pygame.K_RIGHT]:
                self.catcher.move(5)

            self.balls.update()

            hits = pygame.sprite.spritecollide(self.catcher, self.balls, True)
            if hits:
                self.score += len(hits)
                self.lives += len(hits)  # Add 1 to lives for each ball caught
            else:
                self.lives -= 1  # Subtract 1 life if a ball is missed

            if self.lives <= 0:
                self.game_over = True

            self.balls.add(Ball(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)))  # Continuously generate new balls

        self.screen.fill((0, 0, 0))  # Black background
        self.balls.draw(self.screen)
        self.catcher.draw(self.screen)
        self.display_score()

        if self.game_over:
            self.display_game_over()

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

