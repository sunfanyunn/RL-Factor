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
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT))
        self.speed = 10

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, SCREEN_WIDTH - CATCHER_WIDTH)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, -BALL_SIZE))

    def update(self):
        self.rect.y += BALL_FALL_SPEED
        if self.rect.y > SCREEN_HEIGHT:
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
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        new_ball = Ball(x)
        self.balls.add(new_ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.move(-self.catcher.speed)
            if keys[pygame.K_RIGHT]:
                self.catcher.move(self.catcher.speed)

            self.balls.update()
            self.screen.fill((0, 0, 0))
            self.balls.draw(self.screen)
            self.screen.blit(self.catcher.image, self.catcher.rect)

            collisions = pygame.sprite.spritecollide(self.catcher, self.balls, True)
            for _ in collisions:
                self.score += 1
                self.spawn_ball()

            balls_missed = [ball for ball in self.balls if ball.rect.y > SCREEN_HEIGHT]
            for _ in balls_missed:
                self.lives -= 1
                self.spawn_ball()
            self.balls.remove(balls_missed)

            if self.lives <= 0:
                self.game_over = True

            # display the score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            # display the lives
            lives_text = font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 50))

        else:
            font = pygame.font.Font(None, 74)
            game_over_text = font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    game.quit_game()
