import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 5
PIPE_FREQUENCY = 1500


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.velocity = 0
            self.rect.bottom = SCREEN_HEIGHT

    def flap(self):
        self.velocity = FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, inverted=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midtop=(x, SCREEN_HEIGHT if inverted else 0))
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y -= PIPE_HEIGHT
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.pipes = pygame.sprite.Group()
        self.last_pipe = pygame.time.get_ticks()
        self._generate_pipe()

    def _generate_pipe(self):
        pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        bottom_pipe = Pipe(SCREEN_WIDTH)
        bottom_pipe.rect.top = pipe_height + PIPE_GAP
        top_pipe = Pipe(SCREEN_WIDTH, True)
        top_pipe.rect.bottom = pipe_height
        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def check_for_pipe(self):
        now = pygame.time.get_ticks()
        if now - self.last_pipe > PIPE_FREQUENCY:
            self._generate_pipe()
            self.last_pipe = now

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
            self.bird.flap()

        if not self.game_over:
            self.check_for_pipe()
            self.all_sprites.update()

            if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True
            else:
                for pipe in self.pipes:
                    if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                        pipe.passed = True
                        self.score += 1

            self.screen.fill((135, 206, 235))
            self.all_sprites.draw(self.screen)
            score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))
        elif self.game_over:
            game_over_text = self.font.render('Game Over!', True, (200, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()
        self.clock.tick(30)
        return True

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()
