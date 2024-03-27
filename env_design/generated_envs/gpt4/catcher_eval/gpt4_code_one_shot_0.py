
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

pygame.init()


class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))  # White catcher
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def update(self, x):
        self.rect.x = x
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))  # Prevents moving beyond screen


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_DIAMETER, BALL_DIAMETER))
        self.image.fill((255, 0, 0))  # Red ball
        self.rect = self.image.get_rect(center=(x, BALL_RADIUS))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed






class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()
        self.running = True

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.balls = [Ball(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS))]
        self.all_sprites = pygame.sprite.Group(self.balls + [self.catcher])

    def run(self, event):
        while not self.game_over and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.update(self.catcher.rect.x - 5)
            if keys[pygame.K_RIGHT]:
                self.catcher.update(self.catcher.rect.x + 5)

            for ball in self.balls:
                ball.update()
                if ball.rect.top > SCREEN_HEIGHT:
                    self.balls.remove(ball)
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.balls.append(Ball(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)))
                elif pygame.sprite.collide_rect(self.catcher, ball):
                    self.balls.remove(ball)
                    self.score += 1
                    self.balls.append(Ball(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)))

            self.all_sprites = pygame.sprite.Group(self.balls + [self.catcher])

            self.screen.fill((0, 0, 0))  # Black background
            self.all_sprites.draw(self.screen)
            self.display_score()

            if self.game_over:
                self.display_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        return self.running

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        restart_text = self.font.render('Press SPACE to restart', True, (255, 255, 255))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))

if __name__ == "__main__":
    game_instance = Game()
    game_instance.run(None)
    pygame.quit()

