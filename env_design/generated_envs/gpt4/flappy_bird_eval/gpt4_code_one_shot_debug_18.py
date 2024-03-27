import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
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
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.jump()

        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top=False):
        super().__init__()
        height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        if is_top:
            self.rect = self.image.get_rect(midbottom=(x, 0))
        else:
            self.rect = self.image.get_rect(midtop=(x, SCREEN_HEIGHT))

        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVEMENT
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset_game()
    
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(BIRD_X_POSITION, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.pipes = pygame.sprite.Group()
        self.spawn_pipe()
    
    def spawn_pipe(self):
        x_position = SCREEN_WIDTH + PIPE_WIDTH // 2
        top_pipe = Pipe(x_position, is_top=True)
        bottom_pipe = Pipe(x_position)
        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def run(self, event):
        self.screen.fill((135, 206, 235))
        self.all_sprites.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN):
                self.bird.jump()

        if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

        if self.game_over:
            self.display_game_over()
            return not self.game_over

        pipe_list = self.pipes.sprites()
        for pipe in pipe_list:
            if not pipe.passed and pipe.rect.centerx < self.bird.rect.centerx:
                self.score += 0.5
                pipe.passed = True
            if pipe.rect.right < 0 and not pipe.passed:
                self.spawn_pipe()

        self.pipes.update()
        self.all_sprites.draw(self.screen)
        self.display_score()
        pygame.display.flip()
        self.clock.tick(60)
        return not self.game_over

    def display_game_over(self):
        font = pygame.font.SysFont(None, 74)
        text = font.render('Game Over!', True, (200, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    def display_score(self):
        font = pygame.font.SysFont(None, 33)
        text = font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

if __name__ == "__main__":
    game = Game()
    while game.running:
        event = pygame.event.poll()
        game.running = game.run(event)
    pygame.quit()
