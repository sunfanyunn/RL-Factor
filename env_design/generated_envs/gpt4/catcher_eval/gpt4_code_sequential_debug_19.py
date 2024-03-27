import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 150
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5
FONT_SIZE = 36
LIVES = 3
SPAWN_BALL_EVENT = pygame.USEREVENT + 1
DIFFICULTY_INCREASE_THRESHOLD = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 30))

    def move(self, movement):
        self.rect.x += movement
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = BALL_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = LIVES
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        self.balls = pygame.sprite.Group()
        self.spawn_ball()
        pygame.time.set_timer(SPAWN_BALL_EVENT, 2000)

    def spawn_ball(self):
        new_ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def adjust_difficulty(self):
        if self.score % DIFFICULTY_INCREASE_THRESHOLD == 0:
            global BALL_SPEED, CATCHER_WIDTH
            BALL_SPEED += 1
            CATCHER_WIDTH = max(CATCHER_WIDTH - 10, 50)
            self.catcher.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
            self.catcher.image.fill((255, 0, 0))
            self.catcher.rect = self.catcher.image.get_rect(midbottom=(self.catcher.rect.centerx, SCREEN_HEIGHT - 30))

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.catcher.move(-10)
            elif event.key == pygame.K_RIGHT:
                self.catcher.move(10)
        elif event.type == SPAWN_BALL_EVENT:
            self.spawn_ball()

        if not self.game_over:
            self.all_sprites.update()
            caught_balls = pygame.sprite.spritecollide(self.catcher, self.balls, True)
            for ball in caught_balls:
                self.score += 1
                self.adjust_difficulty()

            # Update the balls to remove those that have gone past the bottom of the screen
            for ball in list(self.balls):
                if ball.rect.bottom > SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                    if self.lives <= 0:
                        self.game_over = True

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)

            score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 0))
            self.screen.blit(score_text, (10, 10))

            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 0))
            self.screen.blit(lives_text, (10, 50))
        else:
            game_over_text = self.font.render('Game Over! Click to Restart', True, (255, 255, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))

        pygame.display.flip()
        self.clock.tick(60)

        return True

if __name__ == "__main__":
    pygame.font.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif game.game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                game.reset_game()
            else:
                running = game.run(event)
    pygame.quit()
