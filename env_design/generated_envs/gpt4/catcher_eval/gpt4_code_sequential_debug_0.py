import pygame
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
FONT_SIZE = 30
BALL_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 10))

    def update(self, x_change):
        self.rect.x += x_change
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = BALL_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def spawn_ball(self):
        ball_x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        new_ball = Ball(ball_x)
        self.all_sprites.add(new_ball)
        self.balls.add(new_ball)

    def run(self, event):
        self.clock.tick(60)
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

        if not self.game_over:
            x_change = 0
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                x_change = -10
            if pressed_keys[pygame.K_RIGHT]:
                x_change = 10

            self.catcher.update(x_change)
            self.balls.update()

            collisions = pygame.sprite.spritecollide(self.catcher, self.balls, dokill=True)
            self.score += len(collisions)
            if len(self.balls) == 0:
                self.spawn_ball()

            for ball in list(self.balls):
                if ball.rect.bottom >= SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives <= 0:
                        self.game_over = True
                        break
                    self.spawn_ball()

        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        if self.game_over:
            game_over_message = 'Game Over! Click to continue'
            game_over_text = self.font.render(game_over_message, True, (255, 55, 55))
            game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, game_over_text_rect)

            if pygame.mouse.get_pressed()[0]:
                self.reset_game()

        pygame.display.flip()
        return True

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
