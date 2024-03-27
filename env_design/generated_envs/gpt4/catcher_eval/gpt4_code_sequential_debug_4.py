import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CATCHER_WIDTH = 150
CATCHER_HEIGHT = 20
BALL_SIZE = 25
BALL_SPEED_INITIAL = 5
BALL_ACCELERATION = 0.1


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 50):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))

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
    def __init__(self, x=random.randint(0, SCREEN_WIDTH - BALL_SIZE), y=0, speed=BALL_SPEED_INITIAL):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = speed

    def update(self):
        self.rect.y += self.velocity
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.catcher = Catcher()
        self.balls = pygame.sprite.Group()
        self.current_ball_speed = BALL_SPEED_INITIAL
        self.current_catcher_width = CATCHER_WIDTH
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.current_ball_speed = BALL_SPEED_INITIAL
        self.current_catcher_width = CATCHER_WIDTH
        self.balls.empty()
        self.spawn_ball()

    def spawn_ball(self):
        new_ball = Ball(speed=self.current_ball_speed)
        self.balls.add(new_ball)

    def run(self, event):
        pressed_keys = pygame.key.get_pressed()

        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.game_over_rect.collidepoint(pos):
                    self.reset_game()
            return True

        self.catcher.update(pressed_keys)
        self.balls.update()

        for ball in self.balls:
            if ball.rect.bottom >= SCREEN_HEIGHT:
                self.lives -= 1
                ball.kill()
                if self.lives <= 0:
                    self.game_over = True
                    break
                self.spawn_ball()

        if pygame.sprite.spritecollide(self.catcher, self.balls, True):
            self.score += 1
            self.spawn_ball()
            # Increasing game difficulty based on score
            if self.score % 10 == 0:  # Every 10 points
                self.current_ball_speed += BALL_ACCELERATION
                self.current_catcher_width = max(20, self.current_catcher_width - 5)
                self.catcher.image = pygame.Surface((self.current_catcher_width, CATCHER_HEIGHT))
                self.catcher.image.fill((255, 255, 255))
                self.catcher.rect.width = self.current_catcher_width

        self.screen.fill((0, 0, 0))
        for entity in self.balls:
            self.screen.blit(entity.image, entity.rect)
        self.screen.blit(self.catcher.image, self.catcher.rect)

        score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 50))

        if self.game_over:
            game_over_message = 'Game Over! Click to restart.'
            self.game_over_render = self.font.render(game_over_message, True, (255, 255, 255))
            self.game_over_rect = self.game_over_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(self.game_over_render, self.game_over_rect)

        pygame.display.flip()
        self.clock.tick(30)

        return True


if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            game.run(event)
    pygame.quit()

