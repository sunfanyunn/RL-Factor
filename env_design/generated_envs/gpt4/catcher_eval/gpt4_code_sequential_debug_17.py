import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 150
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_FALL_SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([CATCHER_WIDTH, CATCHER_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))
        self.speed = 5

    def move(self, x_change):
        self.rect.x += x_change
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=(x, -BALL_SIZE // 2))
        self.speed_y = BALL_FALL_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher_group = pygame.sprite.Group(Catcher(SCREEN_WIDTH // 2))
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        new_ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
        self.balls.add(new_ball)

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        catcher = self.catcher_group.sprite
        if keys[pygame.K_LEFT]:
            catcher.move(-catcher.speed)
        if keys[pygame.K_RIGHT]:
            catcher.move(catcher.speed)

        self.balls.update()

        if not self.game_over:
            if pygame.sprite.spritecollide(catcher, self.balls, True):
                self.score += 1
                self.spawn_ball()

            for ball in self.balls:
                if ball.rect.top > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    self.spawn_ball()
                    if self.lives <= 0:
                        self.game_over = True
                        break

        self.screen.fill(WHITE)
        self.catcher_group.draw(self.screen)
        self.balls.draw(self.screen)
        self.display_game_info()

        if self.game_over:
            self.display_game_over()

        pygame.display.flip()
        self.clock.tick(60)

        if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
            x, y = pygame.mouse.get_pos()
            self.reset_game()

    def display_game_info(self):
        score_text = self.font.render(f'Score: {self.score}', True, BLACK)
        lives_text = self.font.render(f'Lives: {self.lives}', True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

    def display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, BLACK)
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.screen.blit(game_over_text, (center_x - game_over_text.get_width() // 2, center_y - game_over_text.get_height() // 2))
        restart_text = self.font.render('Click to Restart', True, BLACK)
        self.screen.blit(restart_text, (center_x - restart_text.get_width() // 2, center_y + game_over_text.get_height() + 10))


if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
