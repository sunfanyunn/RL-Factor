import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 1
BIRD_JUMP = 10
PIPE_SPEED = 5
PIPE_GAP = 200
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_INTERVAL = 1500 # in milliseconds


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Check if bird hits the bottom of the window
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

    def jump(self):
        self.velocity = -BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, upper=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        if upper:
            self.rect.bottom = 0
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = [Pipe(SCREEN_WIDTH + 100, False), Pipe(SCREEN_WIDTH + 100, True)]
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.pipe_sprites = pygame.sprite.Group(self.pipes)
        for pipe in self.pipes:
            self.all_sprites.add(pipe)
        self.last_pipe_time = pygame.time.get_ticks()

    def spawn_pipe(self):
        gap_y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        bottom_pipe = Pipe(SCREEN_WIDTH, False)
        bottom_pipe.rect.top = gap_y + PIPE_GAP
        top_pipe = Pipe(SCREEN_WIDTH, True)
        top_pipe.rect.bottom = gap_y
        self.pipe_sprites.add(bottom_pipe, top_pipe)
        self.all_sprites.add(bottom_pipe, top_pipe)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        
        if not self.game_over:
            self.all_sprites.update()

            if pygame.time.get_ticks() - self.last_pipe_time > PIPE_INTERVAL:
                self.spawn_pipe()
                self.last_pipe_time = pygame.time.get_ticks()

            if pygame.sprite.spritecollide(self.bird, self.pipe_sprites, False):
                self.game_over = True
            else:
                # Check if bird passed the pipe
                for pipe in self.pipe_sprites:
                    if pipe.rect.right < self.bird.rect.left and not pipe.passed:
                        self.score += 0.5 # Each pair of pipes gives 1 point
                        pipe.passed = True

            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            score_text = self.font.render(str(int(self.score)), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            # If bird hits the bottom or top
            if self.bird.rect.top <= 0 or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.bird.jump()
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                self.reset_game()

        else:
            self.screen.fill((0, 0, 0))
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()
        self.clock.tick(30)
        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.reset_game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
