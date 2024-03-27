import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
BIRD_SIZE = 50
GRAVITY = 1
BIRD_FLAP_POWER = 12
PIPE_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BIRD_SIZE, BIRD_SIZE])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity = 0
            self.kill()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height, position):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        if position == 'top':
            self.rect = self.image.get_rect(midbottom=(x, 0))
        else:
            self.rect = self.image.get_rect(midtop=(x, SCREEN_HEIGHT))
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
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.create_pipe_pair()
        pygame.time.set_timer(pygame.USEREVENT+1, 1500)

    def create_pipe_pair(self):
        pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        top_height = SCREEN_HEIGHT - pipe_height - PIPE_GAP
        self.pipes.add(Pipe(SCREEN_WIDTH, pipe_height, 'bottom'))
        self.pipes.add(Pipe(SCREEN_WIDTH, top_height, 'top'))
        # Update all_sprites group with the new pipes
        self.all_sprites.add(self.pipes)

    def run(self, event):
        if not self.game_over:
            if event.type == pygame.USEREVENT+1:
                self.create_pipe_pair()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                self.bird.velocity = -BIRD_FLAP_POWER

            self.bird.update()
            self.pipes.update()
            self.all_sprites.update()

            if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True

            for pipe in self.pipes:
                if pipe.rect.left < self.bird.rect.left and not pipe.passed:
                    pipe.passed = True
                    self.score += 1

            self.screen.fill((255, 255, 255))
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, sprite.rect)
            self.display_score()
            pygame.display.flip()
        else:
            self.display_game_over()
        self.clock.tick(30)

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
        rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, rect.topleft)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
    pygame.quit()
