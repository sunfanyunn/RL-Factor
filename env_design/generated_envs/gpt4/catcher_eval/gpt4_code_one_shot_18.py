import pygame
import sys
import random

# Initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_FALL_SPEED = 5


# Catcher class inheriting from pygame.sprite.Sprite
class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 30))

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - CATCHER_WIDTH))


# Ball class inheriting from pygame.sprite.Sprite
class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, 0))

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
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = [Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE))]
        self.balls_group = pygame.sprite.Group(self.balls)
        self.catcher_group = pygame.sprite.GroupSingle(self.catcher)

    def spawn_ball(self):
        x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
        ball = Ball(x)
        self.balls_group.add(ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-10)
        if keys[pygame.K_RIGHT]:
            self.catcher.move(10)

        self.balls_group.update()
        self.catcher_group.update()

        for ball in list(self.balls_group):
            if ball.rect.top > SCREEN_HEIGHT:
                self.balls_group.remove(ball)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    self.spawn_ball()

        collisions = pygame.sprite.groupcollide(self.balls_group, self.catcher_group, True, False)
        if collisions:
            self.score += len(collisions)
            self.spawn_ball()

        self.screen.fill((0, 0, 0))
        self.balls_group.draw(self.screen)
        self.catcher_group.draw(self.screen)

        # Draw the score
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))

        # Draw the lives
        lives_surf = font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_surf, (10, 50))

        if self.game_over:
            game_over_surf = font.render('Game Over!', True, (255, 255, 255))
            game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_surf, game_over_rect)

        pygame.display.flip()
        self.clock.tick(30)
        return True


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
