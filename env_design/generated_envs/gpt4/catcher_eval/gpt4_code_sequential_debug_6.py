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


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2),
                -BALL_SIZE
            )
        )
        self.speed = BALL_FALL_SPEED

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        pygame.time.set_timer(pygame.USEREVENT + 1, 2000)  # New timer event every 2000 milliseconds
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
        new_ball = Ball()
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_game()
        self.render_screen()
        pygame.display.flip()
        self.clock.tick(60)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT + 1:  # Timer event for spawning new balls
            self.spawn_ball()
        elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
            self.reset_game()

    def update_game(self):
        pressed_keys = pygame.key.get_pressed()
        self.catcher.update(pressed_keys)
        self.balls.update()

        for ball in pygame.sprite.spritecollide(self.catcher, self.balls, dokill=True):
            self.score += 1
            # Optional: Increase difficulty by speeding up the fall or reducing catcher size
            self.catcher.surf = pygame.transform.smoothscale(self.catcher.surf, (max(CATCHER_WIDTH - self.score, 20), CATCHER_HEIGHT))
            self.catcher.rect.width = self.catcher.surf.get_width()
            if self.catcher.rect.x + self.catcher.rect.width > SCREEN_WIDTH:
                self.catcher.rect.right = SCREEN_WIDTH
            for each_ball in self.balls:
                each_ball.speed = min(each_ball.speed + 0.1, 20)

        for ball in list(self.balls):
            if ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0) # Stop spawning balls
                    # Display 'Game Over' and halt any further ball updates
                    break
                else:
                    ball.kill()
                    self.spawn_ball()

    def render_screen(self):
        self.screen.fill((0, 0, 0))
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

        if self.game_over:
            self.show_game_over()

    def show_game_over(self):
        game_over_text = self.font.render('Game Over! Click to restart', True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, game_over_text_rect)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
    pygame.quit()

