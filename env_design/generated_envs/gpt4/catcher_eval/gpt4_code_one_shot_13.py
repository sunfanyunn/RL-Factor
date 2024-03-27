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
        self.rect = self.surf.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT))

    def move(self, x):
        self.rect.x += x
        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, SCREEN_WIDTH - CATCHER_WIDTH)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.surf = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(x, 0))

    def update(self):
        self.rect.y += BALL_FALL_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.balls = [Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE))]
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        for ball in self.balls:
            self.all_sprites.add(ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                self.catcher.move(-10)
            if pressed_keys[pygame.K_RIGHT]:
                self.catcher.move(10)

            self.screen.fill((0, 0, 0))

            for ball in self.balls:
                if ball.rect.y >= SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                    self.all_sprites.remove(ball)
                    if self.lives == 0:
                        self.game_over = True
                if ball.rect.colliderect(self.catcher.rect):
                    self.score += 1
                    self.balls.remove(ball)
                    self.all_sprites.remove(ball)

            if len(self.balls) == 0:
                self.balls.append(Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE)))
                self.all_sprites.add(self.balls[-1])

            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)
                if isinstance(entity, Ball):
                    entity.update()

            score_surf = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 10))

            if self.game_over:
                game_over_surf = pygame.font.SysFont(None, 48).render('Game Over!', True, (255, 255, 255))
                self.screen.blit(game_over_surf, (SCREEN_WIDTH//2 - game_over_surf.get_width()//2, SCREEN_HEIGHT//2 - game_over_surf.get_height()//2))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()

        pygame.display.flip()
        self.clock.tick(30)
        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
