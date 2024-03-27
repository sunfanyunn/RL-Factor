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
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 30))

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, 0))

    def update(self):
        self.rect.y += BALL_FALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls_group = pygame.sprite.Group()
        self.catcher_group = pygame.sprite.GroupSingle(self.catcher)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        if not self.balls_group:
            self.spawn_ball()

    def spawn_ball(self):
        ball = Ball()
        self.balls_group.add(ball)

    def run(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-10)
        if keys[pygame.K_RIGHT]:
            self.catcher.move(10)

        if not self.game_over:
            self.balls_group.update()

            for ball in list(self.balls_group):
                if ball.rect.top > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives <= 0:
                        self.game_over = True
                        break
                    else:
                        self.spawn_ball()

            collisions = pygame.sprite.spritecollide(self.catcher, self.balls_group, dokill=True)
            if collisions:
                self.score += len(collisions)
                self.spawn_ball()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if self.screen.get_rect().collidepoint(pos):
                    self.reset_game()

        self.screen.fill((0, 0, 0))
        self.balls_group.draw(self.screen)
        self.catcher_group.draw(self.screen)

        score_surf = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))

        lives_surf = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_surf, (10, 50))

        if self.game_over:
            game_over_surf = self.font.render('Game Over! Click to restart', True, (255, 255, 255))
            game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_surf, game_over_rect)

        pygame.display.flip()
        self.clock.tick(30)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()
