import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_MOVEMENT_X = 5
PIPE_FREQUENCY = 1500
BIRD_START_X = 100
BIRD_START_Y = 500
GRAVITY = 0.25
BIRD_JUMP_STRENGTH = -10
PIPE_GAP = 200


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
            self.kill() # Game over when bird hits the ground

    def jump(self):
        self.velocity = BIRD_JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, position, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        if position == 'bottom':
            self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT - height))
        else:
            self.rect = self.image.get_rect(topleft=(x, 0))
            self.rect.bottom = SCREEN_HEIGHT - height - PIPE_GAP
        
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVEMENT_X
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.bird = Bird(BIRD_START_X, BIRD_START_Y)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.pipes = pygame.sprite.Group()
        self.game_over = False
        self.last_pipe_spawn_time = pygame.time.get_ticks()
        self.score = 0

    def spawn_new_pipe(self):
        gap_position = random.randint(int(PIPE_GAP * 1.5), SCREEN_HEIGHT - int(PIPE_GAP * 1.5))
        bottom_pipe_height = SCREEN_HEIGHT - gap_position + PIPE_GAP // 2
        top_pipe_height = gap_position - PIPE_GAP // 2

        pipe_top = Pipe(SCREEN_WIDTH, 'top', top_pipe_height)
        pipe_bottom = Pipe(SCREEN_WIDTH, 'bottom', bottom_pipe_height)
        self.pipes.add(pipe_top, pipe_bottom)
        self.all_sprites.add(pipe_top, pipe_bottom)

        self.last_pipe_spawn_time = pygame.time.get_ticks()

    def run(self, event):
        if not self.game_over and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.bird.jump()

        now = pygame.time.get_ticks()
        if now - self.last_pipe_spawn_time > PIPE_FREQUENCY:
            self.spawn_new_pipe()

        self.all_sprites.update()

        if pygame.sprite.spritecollideany(self.bird, self.pipes) or not self.bird.alive():
            self.game_over = True

        self.screen.fill((255, 255, 255))
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {int(self.score)}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()

        # Update score and remove passed pipes
        pipes_to_remove = []
        for pipe in self.pipes:
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                self.score += 0.5  # Count each pipe once
                pipe.passed = True
            if pipe.rect.right < 0:
                pipes_to_remove.append(pipe)
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
            self.all_sprites.remove(pipe)

        self.clock.tick(30)

        return not self.game_over

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()

