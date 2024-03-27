import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5
MIN_SPAWN_DELAY = 500
MAX_SPAWN_DELAY = 1500


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(x, 0))
        self.speed = BALL_SPEED

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.spawn_ball_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_ball_event, random.randint(MIN_SPAWN_DELAY, MAX_SPAWN_DELAY))
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.catcher)
        self.create_ball()

    def create_ball(self):
        ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
        self.balls.add(ball)
        self.all_sprites.add(ball)

    def run(self, event):
        if event is None or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == self.spawn_ball_event:
            self.create_ball()
            pygame.time.set_timer(self.spawn_ball_event, random.randint(MIN_SPAWN_DELAY, MAX_SPAWN_DELAY))

        if not self.game_over:
            pressed_keys = pygame.key.get_pressed()
            self.catcher.update(pressed_keys)
            self.balls.update()

            if pygame.sprite.spritecollideany(self.catcher, self.balls):
                ball = pygame.sprite.spritecollideany(self.catcher, self.balls)
                self.score += 1
                if self.score % 5 == 0:
                    self.catcher.surf = pygame.transform.smoothscale(self.catcher.surf, (self.catcher.rect.width - 5, CATCHER_HEIGHT))
                    self.catcher.rect = self.catcher.surf.get_rect(center=(self.catcher.rect.centerx, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))
                ball.kill()

            for ball in self.balls:
                if ball.rect.bottom >= SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives <= 0:
                        self.game_over = True

            global BALL_SPEED
            BALL_SPEED = min(20, BALL_SPEED + self.score // 10)
            for ball in self.balls:
                ball.speed = BALL_SPEED

            self.screen.fill((0, 0, 0))
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            text_surface = self.font.render(f'Score: {self.score} Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10))

            pygame.display.flip()
        else:
            self.screen.fill((0, 0, 0))
            game_over_surface = self.font.render('Game Over! Click to restart', True, (255, 255, 255))
            self.screen.blit(game_over_surface, ((SCREEN_WIDTH - game_over_surface.get_width()) // 2, (SCREEN_HEIGHT - game_over_surface.get_height()) // 2))
            pygame.display.flip()

            waiting_for_restart = True
            while waiting_for_restart:
                ev = pygame.event.wait()
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_game()
                    waiting_for_restart = False

        self.clock.tick(30)
        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type != pygame.NOEVENT:
            running = game.run(event)
        else:
            running = game.run(None)
    pygame.quit()

