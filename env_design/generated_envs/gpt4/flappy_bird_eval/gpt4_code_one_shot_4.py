
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
GRAVITY = 1
JUMP_HEIGHT = 12
PIPE_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.y >= SCREEN_HEIGHT - BIRD_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - BIRD_HEIGHT

    def jump(self):
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top=False):
        super().__init__()
        height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        if is_top:
            self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP))
            self.rect = self.image.get_rect(topright=(x, 0))
        else:
            self.image = pygame.Surface((PIPE_WIDTH, height))
            self.rect = self.image.get_rect(bottomleft=(x, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))  # green color
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.Font(None, 74)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.bird.jump()

        if not self.game_over:
            self.screen.fill((135, 206, 250))  # Sky blue color

            self.all_sprites.update()

            if not self.pipes or self.pipes.sprites()[-1].rect.right < SCREEN_WIDTH - 3 * PIPE_WIDTH:
                top_pipe = Pipe(SCREEN_WIDTH + PIPE_WIDTH, True)
                bottom_pipe = Pipe(SCREEN_WIDTH + PIPE_WIDTH)
                self.pipes.add(top_pipe)
                self.pipes.add(bottom_pipe)
                self.all_sprites.add(top_pipe)
                self.all_sprites.add(bottom_pipe)

            for pipe in self.pipes:
                if pipe.rect.right < self.bird.rect.left and not pipe.passed:
                    pipe.passed = True
                    self.score += 1

            self.all_sprites.draw(self.screen)

            if pygame.sprite.spritecollide(self.bird, self.pipes, False):
                self.game_over = True

            if self.game_over:
                game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
                self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))

            score_text = self.font.render(str(self.score), True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))

            self.clock.tick(60)
            pygame.display.update()
        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
