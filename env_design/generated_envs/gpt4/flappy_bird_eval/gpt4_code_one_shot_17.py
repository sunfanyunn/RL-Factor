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
        self.rect = pygame.Rect(x, y, BIRD_WIDTH, BIRD_HEIGHT)
        self.speed = 0

    def update(self):
        self.speed += GRAVITY
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT - BIRD_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - BIRD_HEIGHT
            self.speed = 0

    def flap(self):
        self.speed = -FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, upper):
        super().__init__()
        self.passed = False
        gap_top = random.randint(50, SCREEN_HEIGHT - 50 - PIPE_GAP)
        if upper:
            self.rect = pygame.Rect(x, 0, PIPE_WIDTH, gap_top)
        else:
            self.rect = pygame.Rect(x, gap_top + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)

    def update(self):
        self.rect.x -= PIPE_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 54)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.pipes.append(Pipe(SCREEN_WIDTH, True))
        self.pipes.append(Pipe(SCREEN_WIDTH, False))
        pygame.time.set_timer(pygame.USEREVENT, PIPE_SPAWN_FREQUENCY)

    def run(self, event):
        self.clock.tick(60)
        self.screen.fill((135, 206, 250))  # Sky blue background

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.bird.flap()
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.bird.flap()
            if e.type == pygame.USEREVENT:
                self.pipes.append(Pipe(SCREEN_WIDTH, True))
                self.pipes.append(Pipe(SCREEN_WIDTH, False))

        if not self.game_over:
            self.bird.update()
            for pipe in self.pipes[:]:
                pipe.update()
                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)
                if pipe.rect.left < self.bird.rect.right and not pipe.passed:
                    pipe.passed = True
                    self.score += 0.5  # Each pair of pipes will contribute 1 to the score
                if self.bird.rect.colliderect(pipe.rect):
                    self.game_over = True
                    break

            self.screen.blit(self.font.render(f'Score: {int(self.score)}', True, (255, 255, 255)), (10, 10))
            self.screen.fill((255, 255, 255), self.bird.rect)
            for pipe in self.pipes:
                self.screen.fill((0, 128, 0), pipe.rect)

        else:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(5000)
            return False

        pygame.display.flip()
        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
