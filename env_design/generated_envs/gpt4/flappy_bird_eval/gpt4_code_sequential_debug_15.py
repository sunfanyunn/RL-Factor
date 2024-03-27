import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
BIRD_SIZE = 50
GRAVITY = 0.5
BIRD_JUMP = -12
PIPE_SPEED = 3
PIPE_SPACING = 1500


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, position, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 128, 0))
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
        self.pipe_spawn_time = pygame.time.get_ticks()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.pipes = pygame.sprite.Group()
        self.create_pipe_pair()

    def create_pipe_pair(self):
        pipe_x = SCREEN_WIDTH + PIPE_WIDTH
        gap_start = random.randint(int(SCREEN_HEIGHT * 0.1), int(SCREEN_HEIGHT * 0.6))
        top_pipe_height = gap_start
        bottom_pipe_height = SCREEN_HEIGHT - (gap_start + PIPE_GAP)

        top_pipe = Pipe(pipe_x, 'top', top_pipe_height)
        bottom_pipe = Pipe(pipe_x, 'bottom', bottom_pipe_height)
        self.pipes.add(top_pipe, bottom_pipe)

    def run(self, event):
        if not self.game_over:
            self.handle_events(event)
            self.all_sprites.update()
            self.check_collisions()
            self.pipes.update()
            self.spawn_pipes()
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            self.pipes.draw(self.screen)
            self.display_score()
            pygame.display.flip()
            self.clock.tick(60)
        else:
            self.show_game_over()
            pygame.display.flip()
            self.clock.tick(60)
        return not self.game_over

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            self.bird.jump()

    def spawn_pipes(self):
        if pygame.time.get_ticks() - self.pipe_spawn_time > PIPE_SPACING:
            self.pipe_spawn_time = pygame.time.get_ticks()
            self.create_pipe_pair()

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.pipes, False):
            self.game_over = True
        else:
            for pipe in self.pipes:
                if pipe.rect.right < self.bird.rect.left and not pipe.passed:
                    self.score += 0.5 # Increments by 0.5 to account for two pipes (top and bottom) per pass
                    pipe.passed = True

    def display_score(self):
        score_text = self.font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, game_over_rect)

if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
    pygame.quit()



