import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_WIDTH = 80
PIPE_SPEED = 5
PIPE_GAP = 200
GRAVITY = 1
FLAP_STRENGTH = 12
PIPE_GENERATION_TIME = 1500 # in milliseconds

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BIRD_WIDTH, BIRD_HEIGHT])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def flap(self):
        self.velocity = -FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, bottom=True, height=300):
        super().__init__()
        self.image = pygame.Surface([PIPE_WIDTH, height])
        self.image.fill((0, 255, 0))
        if bottom:
            self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT - height))
        else:
            self.rect = self.image.get_rect(bottomleft=(x, 0))
        self.x = x
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.pipe_timer = pygame.time.get_ticks()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over:
                self.bird.flap()
        if not self.game_over:
            if pygame.mouse.get_pressed()[0]:
                self.bird.flap()
            self.screen.fill((135, 206, 235))
            if pygame.time.get_ticks() - self.pipe_timer > PIPE_GENERATION_TIME:
                pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
                bottom_pipe = Pipe(SCREEN_WIDTH, bottom=True, height=pipe_height)
                top_pipe = Pipe(SCREEN_WIDTH, bottom=False, height=SCREEN_HEIGHT - pipe_height - PIPE_GAP)
                self.pipes.add(bottom_pipe)
                self.pipes.add(top_pipe)
                self.all_sprites.add(bottom_pipe)
                self.all_sprites.add(top_pipe)
                self.pipe_timer = pygame.time.get_ticks()
            for pipe in self.pipes:
                if pipe.rect.right < self.bird.rect.left and not pipe.passed:
                    pipe.passed = True
                    self.score += 1
            self.all_sprites.update()
            for entity in self.all_sprites:
                self.screen.blit(entity.image, entity.rect)
            if pygame.sprite.spritecollideany(self.bird, self.pipes) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True
                self.bird.kill()
            score_text = pygame.font.SysFont('Arial', 30).render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
        else:
            game_over_text = pygame.font.SysFont('Arial', 60).render('Game Over!', True, (255, 255, 255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
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