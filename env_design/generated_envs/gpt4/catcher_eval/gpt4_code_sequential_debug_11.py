import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED_INITIAL = 5
BALL_SPEED_INCREASE = 0.5
BALL_SPAWN_RATE = 2000


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 30):
        super().__init__()
        self.surf = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self, x_change):
        self.rect.move_ip(x_change, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect = self.surf.get_rect(
            center=(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2), 0))
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.ball_speed = BALL_SPEED_INITIAL
        self.all_sprites = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        pygame.time.set_timer(pygame.USEREVENT + 1, BALL_SPAWN_RATE)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_game()
                elif event.type == pygame.USEREVENT + 1:
                    self.spawn_ball()

            x_change = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                x_change -= 5
            if keys[pygame.K_RIGHT]:
                x_change += 5
            self.catcher.update(x_change)

            for ball in self.balls:
                ball.update()
                if ball.rect.bottom > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives <= 0:
                        self.game_over = True
                        break

            if not self.game_over:
                collisions = pygame.sprite.spritecollide(self.catcher, self.balls, True)
                for ball in collisions:
                    self.score += 1
                    self.ball_speed += BALL_SPEED_INCREASE
                    self.spawn_ball()

            self.screen.fill((0, 0, 0))
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            self.display_score()

            if self.game_over:
                self.display_game_over()

            pygame.display.flip()
            self.clock.tick(60)

            return running

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))
        lives_surf = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_surf, (10, 50))

    def display_game_over(self):
        game_over_surf = self.font.render('Game Over! Click to restart.', True, (255, 255, 255))
        self.screen.blit(game_over_surf, (SCREEN_WIDTH // 2 - game_over_surf.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_surf.get_height() // 2))

    def spawn_ball(self):
        new_ball = Ball(self.ball_speed)
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()

