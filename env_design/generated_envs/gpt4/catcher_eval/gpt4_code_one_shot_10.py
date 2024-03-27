import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_DROP_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x, width=CATCHER_WIDTH, height=CATCHER_HEIGHT):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - height))
    
    def update(self, dx):
        self.rect.x += dx
        self.rect.clamp_ip(self.rect.clamp(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, size=BALL_SIZE):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, 0))
    
    def update(self):
        self.rect.y += BALL_DROP_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = [Ball(random.randint(0, SCREEN_WIDTH))]
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        for ball in self.balls:
            self.all_sprites.add(ball)

    def run(self, event):
        while not self.game_over:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            keys = pygame.key.get_pressed()
            dx = 0
            if keys[pygame.K_LEFT]:
                dx = -5
            elif keys[pygame.K_RIGHT]:
                dx = 5
            self.catcher.update(dx)
            for ball in self.balls:
                ball.update()
            self.all_sprites.update()
            for ball in self.balls:
                if self.catcher.rect.colliderect(ball.rect):
                    self.score += 1
                    self.all_sprites.remove(ball)
                    self.balls.remove(ball)
            for ball in self.balls:
                if ball.rect.y > SCREEN_HEIGHT:
                    self.all_sprites.remove(ball)
                    self.balls.remove(ball)
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over = True
            if len(self.balls) == 0:
                self.balls.append(Ball(random.randint(0, SCREEN_WIDTH)))
                self.all_sprites.add(self.balls[-1])
            self.all_sprites.draw(self.screen)
            score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
            lives_text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
            game_over_text = self.font.render('Game Over! Click to Continue', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            if self.game_over:
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            waiting = False
                            self.reset_game()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        game.run(event)
        pygame.display.flip()
    pygame.quit()
