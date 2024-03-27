import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
CATCHER_WIDTH = 100
CATCHER_HEIGHT = 20
BALL_SIZE = 20
BALL_FALL_SPEED = 5


# Catcher class inherits from pygame's Sprite class
class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((CATCHER_WIDTH, CATCHER_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT))
        self.speed = 10

    # Update movement of the catcher based on key presses
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(self.speed, 0)

# Ball class inherits from pygame's Sprite class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect = self.image.get_rect(center=(random.randint(BALL_SIZE // 2, SCREEN_WIDTH - BALL_SIZE // 2), 0))
        self.speed = BALL_FALL_SPEED

    # Update the position of the ball as it falls down
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Game class contains game logic
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    # Reset or initialize the game
    def reset_game(self):
        self.game_over = False
        self.lives = 3
        self.score = 0
        self.catcher = Catcher(SCREEN_WIDTH // 2)
        self.ball_group = pygame.sprite.Group()
        self.catcher_group = pygame.sprite.Group(self.catcher)

    # Main game loop
    def run(self, event):
        self.clock.tick(60)

        keys = pygame.key.get_pressed()
        self.catcher.update(keys)
        self.catcher_group.update()

        if not self.ball_group:
            self.ball_group.add(Ball())
        self.ball_group.update()

        # Check for collisions between catcher and balls
        if pygame.sprite.spritecollide(self.catcher, self.ball_group, True):
            self.score += 1
            self.ball_group.add(Ball())

        # Check for balls that fall out of the screen
        for ball in self.ball_group.copy():
            if ball.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                ball.kill()
                if self.lives > 0:
                    self.ball_group.add(Ball())
                else:
                    self.game_over = True

        if self.game_over:
            self.display_game_over()
            self.check_for_reset(event)
        else:
            self.screen.fill((0, 0, 0))
            self.display_score_and_lives()
            self.catcher_group.draw(self.screen)
            self.ball_group.draw(self.screen)
            pygame.display.flip()

    # Display player score and lives
    def display_score_and_lives(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

    # Display Game Over screen
    def display_game_over(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render('Game Over!', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    # Check if the player clicked to reset the game
    def check_for_reset(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                self.reset_game()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        running = game.run(event)
    pygame.quit()