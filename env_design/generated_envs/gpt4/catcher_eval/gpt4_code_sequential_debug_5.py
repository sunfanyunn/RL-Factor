import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_FALL_SPEED = 5
BALL_SPAWN_FREQUENCY = 2000  # in milliseconds
DIFFICULTY_INCREASE_SCORE = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - CATCHER_HEIGHT * 2):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill(pygame.Color('blue'))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, movement):
        self.rect.x += movement
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x=random.randint(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect(topleft=(x, 0))

    def update(self):
        self.rect.y += BALL_FALL_SPEED


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        self.balls = pygame.sprite.Group()
        self.ball_spawner()
        pygame.time.set_timer(pygame.USEREVENT + 1, BALL_SPAWN_FREQUENCY)

    def ball_spawner(self):
        new_ball = Ball()
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.USEREVENT + 1:
                    self.ball_spawner()

            movement = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                movement -= 10
            if keys[pygame.K_RIGHT]:
                movement += 10
            self.catcher.update(movement)

            self.balls.update()
            if not self.game_over:
                collisions = pygame.sprite.spritecollide(
                    self.catcher, self.balls, dokill=True
                )
                self.score += len(collisions)

                for ball in list(self.balls):
                    if ball.rect.top > SCREEN_HEIGHT:
                        self.lives -= 1
                        ball.kill()

                if self.lives <= 0:
                    self.game_over = True

                if self.score and self.score % DIFFICULTY_INCREASE_SCORE == 0:
                    global BALL_FALL_SPEED
                    BALL_FALL_SPEED += 1  # Increase speed

                self.screen.fill((255, 255, 255))
                self.all_sprites.draw(self.screen)
                self.display_score_and_lives()
                pygame.display.flip()

            if self.game_over:
                self.display_game_over()
                if pygame.mouse.get_pressed()[0]:  # wait for mouse click to reset
                    self.reset_game()

        pygame.quit()
        sys.exit()

    def display_score_and_lives(self):
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f'Score: {self.score}', True, (0, 0, 0))
        lives_surf = font.render(f'Lives: {self.lives}', True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf, (10, 50))

    def display_game_over(self):
        font = pygame.font.SysFont(None, 48)
        game_over_surf = font.render('Game Over! Click to continue.', True, (0, 0, 0))
        game_over_rect = game_over_surf.get_rect()
        game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.screen.fill((255, 255, 255))
        self.screen.blit(game_over_surf, game_over_rect)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
