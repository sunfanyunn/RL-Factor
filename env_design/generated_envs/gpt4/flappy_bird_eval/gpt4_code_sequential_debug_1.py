import pygame
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_SPEED = 5
GRAVITY = 1
BIRD_JUMP = -12


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

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        self.velocity = BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height, invert=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        if invert:
            self.rect.bottomleft = (x, SCREEN_HEIGHT // 2 - PIPE_GAP // 2)
        else:
            self.rect.topleft = (x, SCREEN_HEIGHT // 2 + PIPE_GAP // 2)
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
        self.spawn_pipe()

    def spawn_pipe(self):
        x = SCREEN_WIDTH + PIPE_WIDTH
        height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        pipe1 = Pipe(x, height)
        pipe2 = Pipe(x, SCREEN_HEIGHT - height - PIPE_GAP, invert=True)
        self.pipes.add(pipe1, pipe2)
        self.all_sprites.add(pipe1, pipe2)

    def run(self):
        running = True
        spawn_timer = pygame.time.get_ticks()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not self.game_over and ((event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)):
                    self.bird.jump()

            if not self.game_over:
                self.all_sprites.update()

                current_time = pygame.time.get_ticks()
                if current_time - spawn_timer > 1500:
                    self.spawn_pipe()
                    spawn_timer = current_time

                for pipe in self.pipes:
                    if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                        pipe.passed = True
                        self.score += 1

                self.screen.fill((135, 206, 235))
                self.all_sprites.draw(self.screen)

                score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
                score_text_rect = score_surface.get_rect(topleft=(10, 10))
                self.screen.blit(score_surface, score_text_rect)

                if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                    self.game_over = True

                self.clock.tick(30)
                pygame.display.flip()
            else:
                game_over_surface = self.font.render('Game Over!', True, (255, 0, 0))
                game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(game_over_surface, game_over_rect)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

        pygame.quit()

if __name__ == "__main__":
    Game().run()


