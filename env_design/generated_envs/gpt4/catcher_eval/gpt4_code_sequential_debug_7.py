import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED_START = 5
BALL_SPEED_INCREMENT = 0.5
FONT_SIZE = 30
BALL_SPAWN_TIME = 2000


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH // 2):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT))

    def update(self, movement=0):
        self.rect.x += movement
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.speed = BALL_SPEED_START
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, 0))

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.balls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.catcher)
        self.spawn_new_ball()
        self.last_updated = pygame.time.get_ticks()

    def spawn_new_ball(self):
        x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        new_ball = Ball(x)
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def run(self, event):
        self.handle_events(event)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.update(-10)
        if keys[pygame.K_RIGHT]:
            self.catcher.update(10)

        if not self.game_over:
            self.update_game()
        else:
            self.check_for_restart(event)
        self.draw()
        self.clock.tick(60)
        return True

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def update_game(self):
        self.all_sprites.update()

        caught_balls = pygame.sprite.spritecollide(self.catcher, self.balls, True)
        self.score += len(caught_balls)

        for ball in self.balls:
            if ball.rect.bottom > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True

        current_time = pygame.time.get_ticks()
        if current_time - self.last_updated >= BALL_SPAWN_TIME:
            self.spawn_new_ball()
            self.last_updated = current_time

    def check_for_restart(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)

        score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

        lives_surface = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_surface, (10, 50))

        if self.game_over:
            self.display_game_over()

        pygame.display.flip()

    def display_game_over(self):
        game_over_surface = self.font.render('Game Over! Click to restart.', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()
