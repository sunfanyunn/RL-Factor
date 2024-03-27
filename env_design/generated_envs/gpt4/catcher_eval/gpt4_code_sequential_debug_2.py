import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED_START = 5
BALL_SPEED_INCREASE = 0.5 # Speed increase per spawn
BALL_SPAWN_INTERVAL = 2000  # in milliseconds

class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 10))

    def move(self, dx):
        self.rect.x += dx
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Ball(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 0, 0), [0, 0, BALL_SIZE, BALL_SIZE])
        self.rect = self.image.get_rect(center=(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2), -BALL_SIZE))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.top > SCREEN_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 74)
        self.ball_spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ball_spawn_event, BALL_SPAWN_INTERVAL)
        self.ball_speed = BALL_SPEED_START
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.balls.add(Ball(self.ball_speed))  # Ensure there is always at least one ball

    def run(self, event):
        if self.game_over:
            return self.handle_game_over(event)
        else:
            if event.type == pygame.QUIT:
                return False
            elif event.type == self.ball_spawn_event:
                self.balls.add(Ball(self.ball_speed))  # Add a new ball periodically
                self.ball_speed += BALL_SPEED_INCREASE
            keys = pygame.key.get_pressed()
            self.process_keys(keys)
            self.update_game()
            self.draw_game()
            self.clock.tick(60)
        return True

    def process_keys(self, keys):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx -= 5
        elif keys[pygame.K_RIGHT]:
            dx += 5
        self.catcher.move(dx)

    def update_game(self):
        # Update and spawn balls
        self.balls.update()
        for ball in self.balls:
            if ball.is_off_screen():
                self.lives -= 1
                self.balls.remove(ball)
                if self.lives <= 0:
                    self.game_over = True

        # Check collisions
        hits = pygame.sprite.spritecollide(self.catcher, self.balls, True)
        for _ in hits:  # Increment score and adjust difficulty for each caught ball
            self.score += 1
            self.ball_speed += BALL_SPEED_INCREASE
            if self.catcher.rect.width > 20:  # Optionally reduce catcher size
                self.catcher.image = pygame.transform.scale(self.catcher.image, (self.catcher.rect.width - 1, CATCHER_HEIGHT))
                self.catcher.rect = self.catcher.image.get_rect(center=(self.catcher.rect.centerx, SCREEN_HEIGHT - 10))

    def draw_game(self):
        self.screen.fill((0, 0, 0))
        self.balls.draw(self.screen)
        self.screen.blit(self.catcher.image, self.catcher.rect)
        score_surf = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))
        if self.lives > 0:
            life_surf = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(life_surf, (SCREEN_WIDTH - 200, 10))
        pygame.display.flip()

    def handle_game_over(self, event):
        self.draw_game()
        game_over_surf = self.font.render('Game Over! Click to continue', True, (255, 255, 255))
        game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surf, game_over_rect)
        pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()
            return True
        return True


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()


