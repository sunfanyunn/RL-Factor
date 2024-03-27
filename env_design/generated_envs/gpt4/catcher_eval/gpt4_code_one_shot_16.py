
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
CATCHER_SPEED = 10
SCORE_FONT_SIZE = 32
GAME_OVER_FONT_SIZE = 64


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT / 2))

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-CATCHER_SPEED, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(CATCHER_SPEED, 0)

        # Keep catcher on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(x, BALL_SIZE / 2))

    def update(self):
        self.rect.move_ip(0, BALL_FALL_SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, SCORE_FONT_SIZE)
        self.game_over_font = pygame.font.SysFont(None, GAME_OVER_FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH / 2)
        self.balls = [Ball(random.randint(BALL_SIZE / 2, SCREEN_WIDTH - BALL_SIZE / 2))]
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)

    def run(self, event):
        if self.game_over:
            self.show_game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        if event.type == pygame.QUIT:
            return False

        pressed_keys = pygame.key.get_pressed()
        self.catcher.update(pressed_keys)

        # Create new balls if needed
        if len(self.balls) == 0:
            new_ball = Ball(random.randint(BALL_SIZE / 2, SCREEN_WIDTH - BALL_SIZE / 2))
            self.balls.append(new_ball)
            self.all_sprites.add(new_ball)

        # Update every ball
        for ball in self.balls:
            ball.update()
            if ball.rect.bottom > SCREEN_HEIGHT:
                self.lives -= 1
                ball.kill()
                if self.lives == 0:
                    self.game_over = True

        # Check for collisions
        hit_list = pygame.sprite.spritecollide(self.catcher, self.balls, True)
        for hit in hit_list:
            self.score += 1
            new_ball = Ball(random.randint(BALL_SIZE / 2, SCREEN_WIDTH - BALL_SIZE / 2))
            self.balls.append(new_ball)
            self.all_sprites.add(new_ball)

        self.screen.fill((0, 0, 0))
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
        score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.lives > 0:
            lives_text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
            self.screen.blit(lives_text, (SCREEN_WIDTH - 110, 10))

        pygame.display.flip()
        self.clock.tick(30)
        return True

    def show_game_over(self):
        game_over_text = self.game_over_font.render('Game Over!', True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2))
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
