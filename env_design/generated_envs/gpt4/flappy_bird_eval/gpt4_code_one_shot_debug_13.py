import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
GRAVITY = 1
FLAP_STRENGTH = -12
PIPE_SPEED = 5
FRAME_RATE = 60

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top):
        super().__init__()
        height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        if is_top:
            self.rect.bottomleft = (x, 0)
        else:
            self.rect.topleft = (x, SCREEN_HEIGHT - height)
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
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.spawn_pipe()

    def spawn_pipe(self):
        pipe_x = SCREEN_WIDTH + 100
        top_pipe = Pipe(pipe_x, True)
        bottom_pipe = Pipe(pipe_x, False)
        self.pipes.add(top_pipe)
        self.pipes.add(bottom_pipe)
        self.all_sprites.add(top_pipe)
        self.all_sprites.add(bottom_pipe)

    def run(self, event):
        if self.game_over:
            self.display_game_over()
            return False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP or e.key == pygame.K_SPACE:
                    self.bird.velocity = FLAP_STRENGTH
            if pygame.mouse.get_pressed()[0]:
                self.bird.velocity = FLAP_STRENGTH

        self.all_sprites.update()
        if pygame.sprite.spritecollideany(self.bird, self.pipes):
            self.game_over = True

        for pipe in self.pipes:
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                self.score += 1
                pipe.passed = True

        self.screen.fill((135, 206, 235))
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        self.clock.tick(FRAME_RATE)

        # Spawn new pipes
        if not any(pipe.rect.right > SCREEN_WIDTH for pipe in self.pipes):
            self.spawn_pipe()

        return True

    def display_game_over(self):
        self.screen.fill((135, 206, 235))
        game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
        rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(game_over_text, rect)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

