import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
GRAVITY = 1
BIRD_JUMP = 12
PIPE_SPEED = 2
PIPE_SPACING = 200
FREQUENCY = 1500

pygame.init()

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, positioned_top=True):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
        self.image.fill(GREEN)
        if positioned_top:
            self.rect = self.image.get_rect(midbottom=(x, random.randint(50, SCREEN_HEIGHT // 2 - PIPE_SPACING // 2)))
        else:
            self.rect = self.image.get_rect(midtop=(x, random.randint(SCREEN_HEIGHT // 2 + PIPE_SPACING // 2, SCREEN_HEIGHT - 50)))
        self.x = float(self.rect.x)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.rect.x = int(self.x)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.spawn_pipe()
        pygame.time.set_timer(pygame.USEREVENT, FREQUENCY)

    def spawn_pipe(self):
        top_pipe = Pipe(SCREEN_WIDTH + PIPE_WIDTH, True)
        bottom_pipe = Pipe(SCREEN_WIDTH + PIPE_WIDTH, False)
        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def run(self, event):
        self.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.USEREVENT:
                self.spawn_pipe()
            if not self.game_over and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.bird.jump()

        if not self.game_over:
            self.all_sprites.update()
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)

            if pygame.sprite.spritecollide(self.bird, self.pipes, False):
                self.game_over = True

            for pipe in self.pipes:
                if pipe.rect.right < 0:
                    pipe.kill()
                if not self.game_over and not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    self.score += 0.5  # since we have two pipes, increment by 0.5 to count as 1
                    pipe.passed = True

            score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
        else:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.update()
        self.clock.tick(60)
        return True


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        running = game.run(None)
    pygame.quit()
