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
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        if is_top:
            self.rect.bottomleft = (x, 0)
        else:
            self.rect.topleft = (x, SCREEN_HEIGHT - self.rect.height)
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
        self.font = pygame.font.SysFont(None, 36)
        
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.spawn_pipe()
        
    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.bird.velocity = FLAP_STRENGTH
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    self.bird.velocity = FLAP_STRENGTH
            self.screen.fill((135, 206, 235))
            self.all_sprites.update()
            self.pipes.update()

            for pipe in self.pipes:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    self.score += 1
                    pipe.passed = True
            if pygame.sprite.spritecollideany(self.bird, self.pipes):
                self.game_over = True
            self.all_sprites.draw(self.screen)
            self.pipes.draw(self.screen)
            score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            pygame.display.flip()
            self.clock.tick(FRAME_RATE)
            if self.game_over:
                self.display_game_over()
        return True

    def spawn_pipe(self):
        pipe_x = SCREEN_WIDTH + 100
        self.pipes.add(Pipe(pipe_x, True))
        self.pipes.add(Pipe(pipe_x, False))
        self.all_sprites.add(self.pipes)

    def display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
        self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
