import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200
BIRD_JUMP_STRENGTH = -10
GRAVITY = 0.5
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_MOVE_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.velocity = 0
            self.rect.bottom = SCREEN_HEIGHT

    def jump(self):
        self.velocity = BIRD_JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, inverted=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topright=(x, 0 if inverted else SCREEN_HEIGHT))
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, PIPE_GAP)
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.LayeredUpdates(self.bird, self.pipes)
        self.last_pipe = pygame.time.get_ticks()
        self.spawn_pipe()

    def spawn_pipe(self):
        pipe_height = random.randint(100, SCREEN_HEIGHT // 2 - PIPE_GAP // 2)
        bottom_pipe = Pipe(SCREEN_WIDTH + PIPE_WIDTH)
        top_pipe = Pipe(SCREEN_WIDTH + PIPE_WIDTH, inverted=True)
        bottom_pipe.rect.top = pipe_height + PIPE_GAP
        top_pipe.rect.bottom = pipe_height
        self.pipes.add(bottom_pipe, top_pipe)
        self.all_sprites.add(bottom_pipe, top_pipe)

    def run(self):
        if self.game_over:
            self.display_message('Game Over!')
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key in [pygame.K_UP, pygame.K_w]):
                self.bird.jump()

        now = pygame.time.get_ticks()
        if now - self.last_pipe > 1500:
            self.spawn_pipe()
            self.last_pipe = now

        self.all_sprites.update()
        if pygame.sprite.spritecollideany(self.bird, self.pipes) or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

        for pipe in self.pipes:
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                pipe.passed = True
                self.score += 1

        self.screen.fill((135, 206, 250))
        self.all_sprites.draw(self.screen)

        # Display score
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(30)
        return True

    def display_message(self, text):
        text_surface = self.font.render(text, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        running = game.run()
