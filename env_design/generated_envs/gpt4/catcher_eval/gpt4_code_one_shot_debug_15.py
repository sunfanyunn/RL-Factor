import pygame
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_SPEED = 5
SCORE_FONT_SIZE = 30
GAME_OVER_FONT_SIZE = 90


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT - 30))
    
    def update(self, direction=None):
        if direction == 'left' and self.rect.left > 0:
            self.rect.x -= 5
        elif direction == 'right' and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, 0))
    
    def update(self):
        self.rect.y += BALL_SPEED


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, SCORE_FONT_SIZE)
        self.game_over_font = pygame.font.SysFont(None, GAME_OVER_FONT_SIZE)
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
        x = random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2)
        new_ball = Ball(x)
        self.balls.add(new_ball)
        self.all_sprites.add(new_ball)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.catcher.update('left')
            if keys[pygame.K_RIGHT]:
                self.catcher.update('right')

            self.all_sprites.update()

            for ball in self.balls:
                if ball.rect.bottom >= SCREEN_HEIGHT:
                    self.lives -= 1
                    ball.kill()
                    if self.lives <= 0:
                        self.game_over = True
                        self.display_game_over()
                        continue
                elif pygame.sprite.collide_rect(self.catcher, ball):
                    self.score += 1
                    ball.kill()
                    self.spawn_ball()

            if len(self.balls) == 0:
                self.spawn_ball()

            self.screen.fill((0, 0, 0))
            self.display_score()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        return True

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score} Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        game_over_text = self.game_over_font.render('Game Over!', True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
