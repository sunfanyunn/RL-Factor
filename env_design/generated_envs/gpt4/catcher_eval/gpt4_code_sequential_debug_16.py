
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
CATCHER_Y = SCREEN_HEIGHT - 40
BALL_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([CATCHER_WIDTH, CATCHER_HEIGHT])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, CATCHER_Y))

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = BALL_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()
            return True
        return False


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.catcher_group = pygame.sprite.GroupSingle()
        self.balls = pygame.sprite.Group()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher_group.add(Catcher(SCREEN_WIDTH // 2))
        self.spawn_ball()

    def spawn_ball(self):
        x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        ball = Ball(x)
        self.balls.add(ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher_group.sprite.move(-10)
            if keys[pygame.K_RIGHT]:
                self.catcher_group.sprite.move(10)

            for ball in self.balls.sprites():
                missed = ball.update()
                if missed:
                    self.lives -= 1
                    self.spawn_ball()
                    if self.lives <= 0:
                        self.game_over = True
                        break

            collided_balls = pygame.sprite.spritecollide(self.catcher_group.sprite, self.balls, True)
            if collided_balls:
                self.spawn_ball()
            self.score += len(collided_balls)

            global BALL_SPEED, CATCHER_WIDTH
            if self.score % 5 == 0 and self.score != 0: # Every 5 points, increase difficulty
                BALL_SPEED += 0.5 # Increase ball speed
                CATCHER_WIDTH = max(20, CATCHER_WIDTH - 5) # Decrease catcher size
                self.catcher_group.sprite.image = pygame.Surface([CATCHER_WIDTH, CATCHER_HEIGHT])
                self.catcher_group.sprite.image.fill((255, 255, 255))

        self.screen.fill((0, 0, 0))
        self.catcher_group.draw(self.screen)
        self.balls.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

        if self.game_over:
            game_over_text = self.font.render('Game Over! Click to restart', True, (255, 255, 255))
            self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))

        pygame.display.flip()
        self.clock.tick(60)

        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game.game_over or event.type == pygame.MOUSEBUTTONDOWN:
                running = game.run(event)
    pygame.quit()

