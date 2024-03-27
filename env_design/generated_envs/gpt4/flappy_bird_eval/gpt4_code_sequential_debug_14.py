import pygame
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP_SIZE = 200
BIRD_SIZE = 50
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_FREQUENCY = 1500  # milliseconds

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.velocity = FLAP_STRENGTH

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, position, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))  # Green color
        if position == 'top':
            self.rect = self.image.get_rect(bottomleft=(x, 0))
        else:  # position == 'bottom'
            self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT - height))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()
        self.last_update = pygame.time.get_ticks()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.bird)

    def spawn_pipe(self):
        gap_y = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP_SIZE)
        height_top = gap_y
        height_bottom = SCREEN_HEIGHT - gap_y - PIPE_GAP_SIZE
        top_pipe = Pipe(SCREEN_WIDTH, 'top', height_top)
        bottom_pipe = Pipe(SCREEN_WIDTH, 'bottom', height_bottom)
        self.pipes.add(top_pipe, bottom_pipe)
        self.all_sprites.add(top_pipe, bottom_pipe)

    def run(self, event):
        self.clock.tick(30)
        if not event or event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

        if not self.game_over:
            self.bird.update()
            now = pygame.time.get_ticks()
            if now - self.last_update >= PIPE_FREQUENCY:
                self.spawn_pipe()
                self.last_update = now
            self.pipes.update()

            for pipe in self.pipes:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 1
                if pygame.sprite.collide_rect(self.bird, pipe):
                    self.game_over = True
                    break

            if not self.bird.alive():
                self.game_over = True

            self.screen.fill((135, 206, 235))
            self.all_sprites.draw(self.screen)
            score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))
        else:
            for sprite in self.all_sprites:
                sprite.kill()

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()
        return not self.game_over

if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if not game.game_over and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN):
                game.bird.velocity = FLAP_STRENGTH

        if not running:  # Break out of the loop if it's set to False
            break

        running = game.run(None)
    pygame.quit()


