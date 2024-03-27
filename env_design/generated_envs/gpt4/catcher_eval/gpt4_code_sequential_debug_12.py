import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 120
CATCHER_HEIGHT = 20
BALL_DIAMETER = 15
BALL_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def move(self, direction):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= 10
        elif direction == 'right' and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 10


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_DIAMETER, BALL_DIAMETER))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x, BALL_DIAMETER // 2))
        self.speed = BALL_SPEED

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
        self.catcher_group = pygame.sprite.GroupSingle(Catcher(SCREEN_WIDTH // 2))
        self.ball_group = pygame.sprite.Group()
        self.ball_group.add(Ball(random.randint(BALL_DIAMETER // 2, SCREEN_WIDTH - BALL_DIAMETER // 2)))

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.catcher_group.sprite.move('left')
                elif event.key == pygame.K_RIGHT:
                    self.catcher_group.sprite.move('right')

        if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()

        if not self.game_over:
            self.ball_group.update()
            collisions = pygame.sprite.spritecollide(self.catcher_group.sprite, self.ball_group, True)
            for ball in collisions:
                self.score += 1
                self.ball_group.add(Ball(random.randint(BALL_DIAMETER // 2, SCREEN_WIDTH - BALL_DIAMETER // 2)))

                if self.score % 10 == 0:
                    for ball in self.ball_group:
                        ball.speed = min(ball.speed + 0.5, 15)

            for ball in list(self.ball_group):
                if ball.rect.bottom > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives <= 0:
                        self.game_over = True
                        break
                    else:
                        self.ball_group.add(Ball(random.randint(BALL_DIAMETER // 2, SCREEN_WIDTH - BALL_DIAMETER // 2)))

            if len(self.ball_group) == 0: # Ensure there's always at least one ball
                self.ball_group.add(Ball(random.randint(BALL_DIAMETER // 2, SCREEN_WIDTH - BALL_DIAMETER // 2)))

        self.screen.fill((255, 255, 255))
        self.catcher_group.draw(self.screen)
        self.ball_group.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f'Lives: {self.lives}', True, (0, 0, 0))
        self.screen.blit(lives_text, (10, 50))

        if self.game_over:
            game_over_text = self.font.render('Game Over! Click to restart', True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, game_over_rect.topleft)

        pygame.display.flip()
        self.clock.tick(60)
        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
