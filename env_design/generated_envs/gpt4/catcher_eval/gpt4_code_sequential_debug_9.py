import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 30))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect = self.image.get_rect(center=(x, 0))

    def update(self):
        self.rect.y += BALL_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Catcher Game')
        self.clock = pygame.time.Clock()
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
        keys = pygame.key.get_pressed()
        self.catcher.update(keys)

        for ball in self.balls[:]:
            ball.update()
            if self.catcher.rect.colliderect(ball.rect):
                self.score += 1
                self.all_sprites.remove(ball)
                self.balls.remove(ball)
                new_ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
                self.balls.append(new_ball)
                self.all_sprites.add(new_ball)
            elif ball.rect.bottom > SCREEN_HEIGHT:
                self.lives -= 1
                self.all_sprites.remove(ball)
                self.balls.remove(ball)
                if self.lives <= 0:
                    self.game_over = True
                    break
                new_ball = Ball(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2))
                self.balls.append(new_ball)
                self.all_sprites.add(new_ball)

        if not self.game_over:
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            self.show_score_and_lives()
            pygame.display.flip()
        else:
            self.display_game_over()

        self.clock.tick(30)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
            self.reset_game()
        return not self.game_over

    def show_score_and_lives(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        lives_text = font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

    def display_game_over(self):
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render('Game Over!', True, (255, 255, 255))
        restart_text = font.render('Click to restart', True, (255, 255, 255))
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
