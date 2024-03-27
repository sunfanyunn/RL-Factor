import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BALL_SIZE = 20
CATCHER_SIZE = 100
INITIAL_BALL_SPEED = 5
CATCHER_SPEED = 10
BALL_FALL_DELAY = 1000
DIFFICULTY_INCREASE_RATE = 0.05 # Arbitrary rate to increase difficulty

pygame.init()

class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([CATCHER_SIZE, 20])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 10))

    def move(self, x_change):
        self.rect.x += x_change
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE], pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.speed = INITIAL_BALL_SPEED
        self.rect = self.image.get_rect(midtop=(x, 0))

    def update(self):
        self.rect.y += self.speed


class Game:
    def __init__(self):
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 55)
        self.catcher_group = pygame.sprite.GroupSingle()
        self.ball_group = pygame.sprite.Group()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.difficulty_mod = 1
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.catcher_group.add(self.catcher)
        self.spawn_ball()
        pygame.time.set_timer(pygame.USEREVENT, BALL_FALL_DELAY)
    
    def spawn_ball(self):
        x_pos = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        new_ball = Ball(x_pos)
        self.ball_group.add(new_ball)

    def run(self, event):
        self.screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.catcher.move(-CATCHER_SPEED)
        if keys[pygame.K_RIGHT]:
            self.catcher.move(CATCHER_SPEED)

        self.ball_group.update()
        self.catcher_group.draw(self.screen)
        self.ball_group.draw(self.screen)

        if pygame.sprite.spritecollide(self.catcher, self.ball_group, True):
            self.score += 1
            self.update_difficulty()
            self.spawn_ball()

        for ball in list(self.ball_group):
            if ball.rect.top > SCREEN_HEIGHT:
                ball.kill()
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                    self.display_game_over()
                else:
                    self.spawn_ball()

        if event.type == pygame.QUIT:
            return False

        if self.game_over:
            self.handle_game_over_events(event)

        self.display_score()
        self.display_lives()

        pygame.display.flip()
        self.clock.tick(60)
        return not self.game_over

    def update_difficulty(self):
        self.difficulty_mod += DIFFICULTY_INCREASE_RATE
        for ball in self.ball_group:
            ball.speed += self.difficulty_mod
        self.catcher.image = pygame.transform.scale(self.catcher.image, (int(CATCHER_SIZE / self.difficulty_mod), 20))
        self.catcher.rect = self.catcher.image.get_rect(midbottom=self.catcher.rect.midbottom)

    def handle_game_over_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.reset_game()

    def display_score(self):
        score_text = f'Score: {self.score}'
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        self.screen.blit(text_surf, (10, 10))

    def display_lives(self):
        lives_text = f'Lives: {self.lives}'
        text_surf = self.font.render(lives_text, True, (255, 255, 255))
        self.screen.blit(text_surf, (10, 70))

    def display_game_over(self):
        game_over_text = 'Game Over! Click or press SPACE to restart.'
        text_surf = self.font.render(game_over_text, True, (255, 0, 0))
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surf, text_rect)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()


