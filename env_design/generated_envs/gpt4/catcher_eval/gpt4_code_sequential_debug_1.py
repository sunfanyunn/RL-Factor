import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 25
BALL_SPEED = 5
FONT_COLOR = (255, 255, 255)


class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(FONT_COLOR)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

    def update(self, movement):
        self.rect.x += movement
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (0, 255, 0), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect = self.image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH - BALL_SIZE), -BALL_SIZE))

    def update(self):
        self.rect.y += BALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.balls = pygame.sprite.Group()
        self.spawn_ball()

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()
            return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

        keys = pygame.key.get_pressed()
        movement = 0
        if keys[pygame.K_LEFT]:
            movement -= 5
        if keys[pygame.K_RIGHT]:
            movement += 5

        self.catcher.update(movement)
        self.balls.update()

        if pygame.sprite.spritecollide(self.catcher, self.balls, True):
            self.score += 1
            self.spawn_ball()

        for ball in self.balls:
            if ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                ball.kill()
                if self.lives > 0:
                    self.spawn_ball()

        if self.lives <= 0:
            self.game_over = True

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.catcher.image, self.catcher.rect)
        self.balls.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, FONT_COLOR)
        lives_text = self.font.render(f'Lives: {self.lives}', True, FONT_COLOR)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over! Press SPACE to restart', True, FONT_COLOR)
            self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def spawn_ball(self):
        new_ball = Ball()
        self.balls.add(new_ball)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
    pygame.quit()
