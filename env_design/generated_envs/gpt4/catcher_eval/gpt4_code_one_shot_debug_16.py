import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_FALL_SPEED = 5
CATCHER_SPEED = 10
SCORE_FONT_SIZE = 32
GAME_OVER_FONT_SIZE = 64


class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-CATCHER_SPEED, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(CATCHER_SPEED, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2), 0))

    def update(self):
        self.rect.move_ip(0, BALL_FALL_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_score = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.font_game_over = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.balls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        self.spawn_ball()

    def spawn_ball(self):
        new_ball = Ball()
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if not self.game_over:
            pressed_keys = pygame.key.get_pressed()
            self.catcher.update(pressed_keys)

            if len(self.balls) < 1:
                self.spawn_ball()

            self.balls.update()

            collided_balls = pygame.sprite.spritecollide(self.catcher, self.balls, dokill=True)
            self.score += len(collided_balls)

            for ball in self.balls:
                if ball.rect.bottom > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives <= 0:
                        self.game_over = True

            self.screen.fill((0, 0, 0))
            score_text = self.font_score.render(f'Score: {self.score}', True, (255, 255, 255))
            lives_text = self.font_score.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)
        else:
            game_over_text = self.font_game_over.render('Game Over!', True, (255, 255, 255))
            self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(30)
        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
