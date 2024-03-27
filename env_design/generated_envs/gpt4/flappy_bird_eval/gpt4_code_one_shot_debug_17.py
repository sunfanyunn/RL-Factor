import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
GRAVITY = 0.5
FLAP_STRENGTH = 10
PIPE_SPEED = 3
PIPE_SPAWN_FREQUENCY = 1500 # milliseconds


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 0

    def update(self):
        self.speed += GRAVITY
        self.rect.y += int(self.speed)
        if self.rect.bottom >= SCREEN_HEIGHT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def flap(self):
        self.speed = -FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, upper):
        super().__init__()
        gap_top = random.randint(50, SCREEN_HEIGHT - 50 - PIPE_GAP)
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))  # Green color
        if upper:
            self.rect = self.image.get_rect(midbottom=(x, gap_top))
        else:
            self.rect = self.image.get_rect(midtop=(x, gap_top + PIPE_GAP))
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
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 54)
        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird_group.empty()
        self.pipe_group.empty()
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)
        pygame.time.set_timer(pygame.USEREVENT, PIPE_SPAWN_FREQUENCY)

    def run(self, event):
        self.clock.tick(60)
        self.screen.fill((135, 206, 250))  # Sky blue background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.bird.flap()
            if event.type == pygame.USEREVENT:
                self.pipe_group.add(Pipe(SCREEN_WIDTH, True))
                self.pipe_group.add(Pipe(SCREEN_WIDTH, False))

        if not self.game_over:
            self.bird_group.update()
            self.pipe_group.update()

            for pipe in self.pipe_group:
                if not pipe.passed and pipe.rect.centerx < self.bird.rect.centerx:
                    pipe.passed = True
                    self.score += 0.5

            if pygame.sprite.spritecollideany(self.bird, self.pipe_group) or self.bird.rect.top <= 0:
                self.game_over = True

            self.bird_group.draw(self.screen)
            self.pipe_group.draw(self.screen)

            self.screen.blit(self.font.render(f'Score: {int(self.score)}', True, (255, 255, 255)), (10, 10))
        else:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.display.flip()
        return True

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        # Handling events by iterating through the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
