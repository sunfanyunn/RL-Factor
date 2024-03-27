import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PIPE_WIDTH = 80
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
BIRD_X = 50
GRAVITY = 0.5
BIRD_JUMP = 12
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self, pipes):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if pygame.sprite.spritecollide(self, pipes, False) or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity = 0
            return True
        return False

    def jump(self):
        self.velocity = -BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, positioned_top=True):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        top_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        bottom_height = SCREEN_HEIGHT - top_height - PIPE_GAP
        if positioned_top:
            pygame.draw.rect(self.image, GREEN, (0, 0, PIPE_WIDTH, top_height))
            self.rect = self.image.get_rect(topleft=(x, 0))
        else:
            pygame.draw.rect(self.image, GREEN, (0, SCREEN_HEIGHT - bottom_height, PIPE_WIDTH, bottom_height))
            self.rect = self.image.get_rect(bottomleft=(x, SCREEN_HEIGHT))
        self.passed = False

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

    def is_bird_passed(self, bird):
        if not self.passed and bird.rect.left > self.rect.right:
            self.passed = True
            return True
        return False


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(BIRD_X, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.pipe_timer = pygame.time.get_ticks()

    def run(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            return False
        if keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.jump()

        if self.game_over:
            if keys[pygame.K_r]:
                self.reset_game()
            return True

        current_time = pygame.time.get_ticks()
        if current_time - self.pipe_timer > PIPE_FREQUENCY:
            self.create_pipe_pair(SCREEN_WIDTH)
            self.pipe_timer = current_time

        self.game_over = self.bird.update(self.pipes)
        self.pipes.update()

        self.check_collisions()

        self.screen.fill(BLACK)
        self.draw_elements()
        pygame.display.flip()
        self.clock.tick(30)
        return True

    def create_pipe_pair(self, x):
        top_pipe = Pipe(x, True)
        bottom_pipe = Pipe(x, False)
        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def check_collisions(self):
        for pipe in self.pipes:
            if pipe.is_bird_passed(self.bird):
                self.score += 1

    def draw_elements(self):
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to reset', True, WHITE)
            self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
