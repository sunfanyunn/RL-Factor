import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_JUMP = -15
GRAVITY = 1
PIPE_GAP = 200
PIPE_FREQUENCY = 1500 # milliseconds
PIPE_SPEED = 5


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

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, upper=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(100, SCREEN_HEIGHT // 2))
        self.image.fill((0, 255, 0))
        if upper:
            self.rect = self.image.get_rect(bottomleft=(x, random.randint(0, SCREEN_HEIGHT // 2 - PIPE_GAP // 2)))
        else:
            self.rect = self.image.get_rect(topleft=(x, self.rect.bottom + PIPE_GAP))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED

        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.reset_game()
        self.font = pygame.font.Font(None, 36)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird_group.empty()
        self.pipe_group.empty()

        # Initialize bird
        self.bird = Bird(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)

        # Initialize first set of pipes
        self.add_pipe()

        # Set up the first pipe generation
        pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)

    def add_pipe(self):
        x = SCREEN_WIDTH + 100
        upper_pipe = Pipe(x, upper=True)
        lower_pipe = Pipe(x, upper=False)

        self.pipe_group.add(upper_pipe)
        self.pipe_group.add(lower_pipe)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        self.screen.fill((135, 206, 250))

        if not self.game_over:
            if event.type == pygame.USEREVENT:
                self.add_pipe()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    self.bird.jump()

            self.bird_group.update()
            self.pipe_group.update()

            self.bird_group.draw(self.screen)
            self.pipe_group.draw(self.screen)

            # Check for collisions
            if pygame.sprite.spritecollide(self.bird, self.pipe_group, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True

            # Scoring
            for pipe in self.pipe_group:
                if not pipe.passed and pipe.rect.centerx < self.bird.rect.centerx:
                    self.score += 1
                    pipe.passed = True

            # Draw score
            score_text = self.font.render(str(self.score), True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
        else:
            # Display game over
            game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.update()
        self.clock.tick(30)

        return not self.game_over

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
