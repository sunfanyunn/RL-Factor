import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_FREQUENCY = 1500
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
GRAVITY = 0.5
FLAP_STRENGTH = -10
BIRD_X_POSITION = SCREEN_WIDTH // 4


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

    def flap(self):
        self.velocity = FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, upward):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(50, SCREEN_HEIGHT // 2 - PIPE_GAP // 2 - 50)))
        self.rect = self.image.get_rect()
        self.image.fill((0, 255, 0))
        self.rect.x = x
        if upward:
            self.rect.bottom = SCREEN_HEIGHT // 2 - PIPE_GAP // 2
        else:
            self.rect.top = SCREEN_HEIGHT // 2 + PIPE_GAP // 2
        self.velocity_x = -5

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.right <= 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36) # Initialize font for the score display
        self.clock = pygame.time.Clock()
        self.bird_group = pygame.sprite.GroupSingle()
        self.pipe_group = pygame.sprite.Group()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(BIRD_X_POSITION, SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)
        self.pipe_group.empty() # Clear existing pipes
        self.last_pipe = pygame.time.get_ticks()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif not self.game_over and (event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP]) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            self.bird.flap()
        elif self.game_over and event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
            self.reset_game()

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.bird_group.update()
            self.pipe_group.update()

            now = pygame.time.get_ticks()
            if now - self.last_pipe > PIPE_FREQUENCY:
                self.spawn_pipe()
                self.last_pipe = now

            for pipe in self.pipe_group:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 1

            if pygame.sprite.spritecollide(self.bird, self.pipe_group, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True

        self.screen.fill((135, 206, 235)) # Sky blue background
        self.bird_group.draw(self.screen)
        self.pipe_group.draw(self.screen)
        self.display_score()

        if self.game_over:
            self.display_game_over()

        pygame.display.flip()
        self.clock.tick(60)

        return not self.game_over

    def spawn_pipe(self):
        upward = random.choice([True, False])
        new_pipe = Pipe(SCREEN_WIDTH, not upward)
        self.pipe_group.add(new_pipe)
        if upward:
            bottom_pipe = Pipe(SCREEN_WIDTH, False)
            bottom_pipe.rect.top = new_pipe.rect.bottom + PIPE_GAP
            self.pipe_group.add(bottom_pipe)

    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(topleft=(10, 10))
        self.screen.blit(score_surface, score_rect)

    def display_game_over(self):
        game_over_surface = self.font.render('Game Over! Press any key to restart', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()

