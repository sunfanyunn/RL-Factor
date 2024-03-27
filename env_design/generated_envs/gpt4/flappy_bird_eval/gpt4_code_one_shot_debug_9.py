import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
GRAVITY = 0.5
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
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        if self.rect.bottom < SCREEN_HEIGHT: # Prevent jumping when bird is on the ground
            self.velocity = -BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
        self.image.fill(GREEN)
        top = random.choice([True, False])
        bottom = not top
        if top:
            self.rect = self.image.get_rect(midbottom=(x, random.randint(50, SCREEN_HEIGHT // 2 - PIPE_SPACING // 2)))
        elif bottom:
            self.rect = self.image.get_rect(midtop=(x, random.randint(SCREEN_HEIGHT // 2 + PIPE_SPACING // 2, SCREEN_HEIGHT - 50)))
        self.x = float(self.rect.x)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.rect.x = int(self.x)

    def is_off_screen(self):
        return self.rect.right < 0


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
        self.all_sprites = pygame.sprite.Group(self.bird)
        pygame.time.set_timer(pygame.USEREVENT, FREQUENCY)
    
    def spawn_pipe(self):
        top_pipe = Pipe(SCREEN_WIDTH)
        bottom_pipe = Pipe(SCREEN_WIDTH)
        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def run(self, event):
        if self.game_over:
            return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.USEREVENT:
                self.spawn_pipe()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.jump()

        self.screen.fill((0, 0, 0))
        self.all_sprites.update()

        for pipe in self.pipes:
            if pipe.is_off_screen():
                pipe.kill()
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                self.score += 1
                pipe.passed = True

        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True
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
