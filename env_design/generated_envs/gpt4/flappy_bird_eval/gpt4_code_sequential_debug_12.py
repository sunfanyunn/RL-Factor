import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_FREQUENCY = 1500
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
FLOOR = SCREEN_HEIGHT - 80
GRAVITY = 0.5
FLAP_STRENGTH = 12
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.bottom >= FLOOR:
            self.rect.bottom = FLOOR
            self.velocity = 0

    def flap(self):
        if self.rect.top > 0:
            self.velocity = -FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, initialized=False):
        super().__init__()
        self.top_pipe_height = random.randint(50, FLOOR - PIPE_GAP)
        self.image = pygame.Surface((PIPE_WIDTH, self.top_pipe_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topright=(x, 0))
        self.passed = False

        # Generate bottom pipe
        bottom_pipe_height = FLOOR - self.top_pipe_height - PIPE_GAP
        self.bottom_pipe_image = pygame.Surface((PIPE_WIDTH, bottom_pipe_height))
        self.bottom_pipe_image.fill(GREEN)
        self.bottom_pipe_rect = self.bottom_pipe_image.get_rect(bottomleft=(x, SCREEN_HEIGHT))

        if initialized:
            self.rect.x -= 2
            self.bottom_pipe_rect.x -= 2

    def update(self):
        self.rect.x -= 2
        self.bottom_pipe_rect.x -= 2

        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.Font(None, 32)
        self.reset_game()
        pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.pipes = pygame.sprite.Group()

    def add_pipe(self):
        pipe = Pipe(SCREEN_WIDTH, initialized=True)
        self.pipes.add(pipe)
        self.all_sprites.add(pipe)

    def run(self, event):
        if self.game_over:
            return False

        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            self.bird.flap()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()
        if event.type == pygame.USEREVENT:
            self.add_pipe()

        self.screen.fill(WHITE)
        self.all_sprites.update()

        for entity in self.all_sprites:
            self.screen.blit(entity.image, entity.rect)
        for pipe in self.pipes:
            self.screen.blit(pipe.bottom_pipe_image, pipe.bottom_pipe_rect)

        if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= FLOOR:
            self.end_game()

        pipe_list = self.pipes.sprites()
        for pipe in pipe_list:
            if pipe.rect.right < self.bird.rect.left and not pipe.passed:
                pipe.passed = True
                self.score += 1

        self.show_score()

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def show_score(self):
        score_surface = self.score_font.render(f'Score: {int(self.score)}', True, BLACK)
        self.screen.blit(score_surface, (10, 10))

    def end_game(self):
        self.game_over = True
        self.show_game_over()

    def show_game_over(self):
        game_over_surface = self.score_font.render('Game Over!', True, BLACK)
        x_centered = SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2
        y_centered = SCREEN_HEIGHT // 2 - game_over_surface.get_height() // 2
        self.screen.blit(game_over_surface, (x_centered, y_centered))
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

