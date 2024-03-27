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
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, SCREEN_HEIGHT - CATCHER_HEIGHT // 2))
        self.speed = 10

    def update(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(SCREEN_WIDTH - CATCHER_WIDTH, self.rect.x))


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, BALL_SIZE // 2))

    def update(self):
        self.rect.y += BALL_FALL_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.balls = [Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE))]

    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            self.screen.fill((0, 0, 0))
            self.catcher.update(event)
            self.screen.blit(self.catcher.image, self.catcher.rect)
            for ball in self.balls:
                ball.update()
                self.screen.blit(ball.image, ball.rect)
                if self.catcher.rect.colliderect(ball.rect):
                    self.score += 1
                    self.balls.remove(ball)
                elif ball.rect.top >= SCREEN_HEIGHT:
                    self.lives -= 1
                    self.balls.remove(ball)
                    if self.lives <= 0:
                        self.game_over = True
                        self.display_game_over()
            if not self.balls:
                self.balls.append(Ball(random.randint(0, SCREEN_WIDTH - BALL_SIZE)))
            self.display_score_and_lives()
            pygame.display.flip()
            self.clock.tick(60)
        return self.handle_game_over()

    def display_score_and_lives(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render('Score: ' + str(self.score), 1, (255, 255, 255))
        lives_text = font.render('Lives: ' + str(self.lives), 1, (255, 255, 255))
        self.screen.blit(score_text, (5, 5))
        self.screen.blit(lives_text, (5, 40))

    def display_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render('Game Over!', 1, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def handle_game_over(self):
        pygame.display.flip()
        wait_for_restart = True
        while wait_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    wait_for_restart = False
        self.reset_game()
        return True


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
