import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PIPE_WIDTH = 80
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_GAP = 200
GRAVITY = 1
JUMP_HEIGHT = -12
PIPE_MOVEMENT = -5
PIPE_SPAWN_TIME = 1500


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
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = GRAVITY

    def jump(self):
        self.velocity = JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, -PIPE_GAP) if is_top else (x, SCREEN_HEIGHT))
        self.rect.y -= self.rect.height if is_top else 0
        self.passed = False

    def update(self):
        self.rect.x += PIPE_MOVEMENT


class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)

        self.pipes = []
        self.pipes.append(Pipe(SCREEN_WIDTH))
        self.pipes.append(Pipe(SCREEN_WIDTH, True))
        for pipe in self.pipes:
            self.pipe_group.add(pipe)

        self.last_pipe_spawn = pygame.time.get_ticks()

    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    return False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if event.key == pygame.K_UP or event.type == pygame.MOUSEBUTTONDOWN:
                        self.bird.jump()

            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe_spawn > PIPE_SPAWN_TIME:
                top_pipe = Pipe(SCREEN_WIDTH, True)
                bottom_pipe = Pipe(SCREEN_WIDTH)
                self.pipe_group.add(top_pipe, bottom_pipe)
                self.last_pipe_spawn = current_time

            self.screen.fill((135, 206, 250))
            self.bird_group.update()
            self.pipe_group.update()

            for pipe in self.pipe_group:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 0.5

            self.bird_group.draw(self.screen)
            self.pipe_group.draw(self.screen)

            for pipe in self.pipe_group:
                if pipe.rect.right <= 0:
                    self.pipe_group.remove(pipe)

            if pygame.sprite.spritecollide(self.bird, self.pipe_group, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True

            score_text = pygame.font.Font(None, 36).render(str(int(self.score)), True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()

            if self.game_over:
                game_over_text = pygame.font.Font(None, 72).render('Game Over!', True, (255, 0, 0))
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(2000)

            self.clock.tick(30)

        return False

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
