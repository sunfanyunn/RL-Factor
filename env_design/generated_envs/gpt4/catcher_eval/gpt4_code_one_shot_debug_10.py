import pygame
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_DROP_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))

    def update(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
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
        self.balls = [Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))]
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)
        for ball in self.balls:
            self.all_sprites.add(ball)

    def run(self, event):
        if self.game_over:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
        else:
            if event.type == pygame.QUIT:
                return False
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            keys = pygame.key.get_pressed()
            dx = 0
            if keys[pygame.K_LEFT]:
                dx = -5
            elif keys[pygame.K_RIGHT]:
                dx = 5
            self.catcher.update(dx)
            for ball in self.balls[:]:
                ball.update()
                if self.catcher.rect.colliderect(ball.rect):
                    self.score += 1
                    self.balls.remove(ball)
                    self.all_sprites.remove(ball)
                elif ball.rect.bottom > SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                    self.all_sprites.remove(ball)
                    if self.lives <= 0:
                        self.game_over = True
            if len(self.balls) == 0:
                new_ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
                self.balls.append(new_ball)
                self.all_sprites.add(new_ball)
            self.all_sprites.draw(self.screen)
            score_text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
            lives_text = self.font.render('Lives: ' + str(self.lives), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            if self.game_over:
                game_over_text = self.font.render('Game Over! Click to Continue', True, (255, 255, 255))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
