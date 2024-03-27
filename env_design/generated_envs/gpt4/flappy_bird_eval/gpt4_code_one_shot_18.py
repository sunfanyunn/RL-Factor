import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_WIDTH = 80
PIPE_GAP = 200
GRAVITY = 1
JUMP_HEIGHT = 12
PIPE_MOVEMENT = 5
BIRD_X_POSITION = SCREEN_WIDTH // 3


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # Filling the bird with a yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Prevent the bird from falling off the screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)))
        self.image.fill((0, 255, 0))  # Filling the pipe with a green color
        self.rect = self.image.get_rect()

        if is_top:
            self.rect.bottomleft = (x, self.rect.height - PIPE_GAP)
        else:
            self.rect.topleft = (x, SCREEN_HEIGHT - self.rect.height)

        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVEMENT

        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(BIRD_X_POSITION, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.spawn_pipe()

    def spawn_pipe(self):
        x_position = SCREEN_WIDTH + PIPE_WIDTH
        top_pipe = Pipe(x_position, True)
        bottom_pipe = Pipe(x_position)
        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def run(self, event):
        self.screen.fill((135, 206, 235))  # Filling the screen with a sky blue color
        self.all_sprites.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if not self.game_over and (event.type == pygame.KEYDOWN and event.key == pygame.K_UP or event.type == pygame.MOUSEBUTTONDOWN):
                self.bird.jump()

        if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True
            self.display_game_over()

        if not self.game_over:
            # Spawn new pipes
            for pipe in self.pipes:
                if pipe.rect.centerx < self.bird.rect.left and not pipe.passed:
                    pipe.passed = True
                    self.spawn_pipe()
                    self.score += 1

        self.all_sprites.draw(self.screen)
        self.display_score()

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def display_game_over(self):
        font = pygame.font.SysFont(None, 74)
        text = font.render('Game Over!', True, (200, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    def display_score(self):
        font = pygame.font.SysFont(None, 33)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run(None)
    pygame.quit()
