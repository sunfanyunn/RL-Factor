import pygame
import sys
import random

# initialize constants
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

    def move(self, x):
        self.rect.x += x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect = self.surf.get_rect(center=(x, 0))

    def update(self):
        self.rect.y += BALL_FALL_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.catcher)
        self.spawn_ball()

    def run(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        if not self.game_over:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                self.catcher.move(-10)
            if pressed_keys[pygame.K_RIGHT]:
                self.catcher.move(10)

            self.balls.update()

            for ball in self.balls:
                if pygame.sprite.collide_rect(ball, self.catcher):
                    self.score += 1
                    ball.kill()
                    self.spawn_ball()
                elif ball.rect.bottom > SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.spawn_ball()

        self.screen.fill((0, 0, 0))
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        score_surf = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))

        if self.game_over:
            game_over_surf = self.font.render('Game Over!', True, (255, 255, 255))
            self.screen.blit(game_over_surf, (SCREEN_WIDTH//2 - game_over_surf.get_width()//2, SCREEN_HEIGHT//2 - game_over_surf.get_height()//2))

        pygame.display.flip()
        self.clock.tick(30)
        return True

    def spawn_ball(self):
        new_ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()