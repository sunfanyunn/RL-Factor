import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_SIZE = (100, 20)
BALL_SIZE = 20
BALL_INITIAL_DROP_SPEED = 5
BALL_SPEED_INCREASE = 0.5
CATCHER_SPEED = 10
CATCHER_MIN_WIDTH = 50
BALL_COLOR = (255, 0, 0)
CATCHER_COLOR = (255, 255, 255)


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH // 2):
        super().__init__()
        self.image = pygame.Surface(CATCHER_SIZE)
        self.image.fill(CATCHER_COLOR)
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 10))

    def move(self, x_change):
        self.rect.x += x_change
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shrink(self):
        if self.rect.width > CATCHER_MIN_WIDTH:
            center = self.rect.center
            self.rect.width -= 10
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill(CATCHER_COLOR)
            self.rect = self.image.get_rect(center=center)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x=None):
        super().__init__()
        if x is None:
            x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, -BALL_SIZE // 2))
        pygame.draw.circle(self.image, BALL_COLOR, (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.speed = BALL_INITIAL_DROP_SPEED
    
    def update(self):
        self.rect.y += self.speed


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.balls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.catcher)
        self.ball_speed = BALL_INITIAL_DROP_SPEED
        self.ball_spawn()

    def ball_spawn(self):
        new_ball = Ball()
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def ball_miss(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
    
    def run(self, event):
        if self.game_over and event and event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()
        if not self.game_over:
            self.screen.fill((0, 0, 0))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.move(-CATCHER_SPEED)
            if keys[pygame.K_RIGHT]:
                self.catcher.move(CATCHER_SPEED)

            self.balls.update()
            for ball in self.balls:
                if self.catcher.rect.colliderect(ball.rect):
                    self.score += 1
                    ball.kill()
                    self.catcher.shrink()
                    self.ball_speed += BALL_SPEED_INCREASE
                    self.ball_spawn()
                elif ball.rect.top >= SCREEN_HEIGHT:
                    ball.kill()
                    self.ball_miss()
                    if not self.game_over:
                        self.ball_spawn()

            self.all_sprites.draw(self.screen)
            score_surf = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 10))
            lives_surf = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(lives_surf, (10, 40))

        else:
            game_over_surf = self.font.render('Game Over! Click to restart.', True, (255, 255, 255))
            game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_surf, game_over_rect)

        pygame.display.flip()
        self.clock.tick(60)
        return not self.game_over

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
