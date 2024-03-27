import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP_SIZE = 200
PIPE_SPEED = 5
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_X_POSITION = SCREEN_WIDTH // 4
GRAVITY = 0.5
JUMP_HEIGHT = -10
FONT_SIZE = 32


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
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

    def jump(self):
        self.velocity = JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, inverted, gap_y):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT if inverted else SCREEN_HEIGHT - gap_y - PIPE_GAP_SIZE // 2))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.topright = (x, 0)
        else:
            self.rect.bottomleft = (x, gap_y + PIPE_GAP_SIZE // 2)
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
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.reset_game()

    def reset_game(self):
        self.bird = Bird(BIRD_X_POSITION, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.game_over = False
        self.score = 0
        self.spawn_pipe()

    def spawn_pipe(self):
        gap_y = random.randint(PIPE_GAP_SIZE // 2, SCREEN_HEIGHT - PIPE_GAP_SIZE // 2)
        x = SCREEN_WIDTH + PIPE_WIDTH
        self.pipes.add(Pipe(x, True, gap_y))
        self.pipes.add(Pipe(x, False, gap_y))
        for pipe in self.pipes:
            self.all_sprites.add(pipe)

    def run(self, event):
        if not self.game_over:
            self.handle_events(event)
            self.update_game()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        return not self.game_over

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif (event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP]) or (event.type == pygame.MOUSEBUTTONDOWN):
            self.bird.jump()

    def update_game(self):
        self.all_sprites.update()
        if pygame.sprite.spritecollideany(self.bird, self.pipes):
            self.game_over = True
        for pipe in list(self.pipes):
            if not pipe.passed and self.bird.rect.left > pipe.rect.right:
                self.score += 1
                pipe.passed = True
            if pipe.rect.right < 0:
                pipe.kill()
        if not self.pipes or all(pipe.rect.right < SCREEN_WIDTH // 2 for pipe in self.pipes):
            self.spawn_pipe()

    def draw(self):
        self.screen.fill((135, 206, 250))
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {int(self.score)}', True, (0, 0, 0))
        self.screen.blit(score_text, (8, 8))
        if self.game_over:
            self.game_over_message()

    def game_over_message(self):
        game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

