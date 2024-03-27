import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 1
JUMP_HEIGHT = 20
PIPE_FREQUENCY = 1500 # in milliseconds
PIPE_GAP = 200
PIPE_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
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
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, gap_center):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, gap_center))
        self.x = x
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.rect.x = self.x


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.SysFont(None, 70)
        self.last_pipe_time = pygame.time.get_ticks()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()

    def spawn_pipe_pair(self):
        gap_center = random.randint(PIPE_GAP, SCREEN_HEIGHT - PIPE_GAP)
        top_pipe = Pipe(SCREEN_WIDTH, gap_center - PIPE_GAP // 2)
        bottom_pipe = Pipe(SCREEN_WIDTH, gap_center + PIPE_GAP // 2)
        self.pipes.add(top_pipe, bottom_pipe)

    def run(self, event):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.bird.jump()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.jump()

            now = pygame.time.get_ticks()
            if now - self.last_pipe_time > PIPE_FREQUENCY:
                self.last_pipe_time = now
                self.spawn_pipe_pair()

            self.bird.update()
            self.pipes.update()

            for pipe in self.pipes:
                if self.bird.rect.colliderect(pipe.rect):
                    self.game_over = True

                if not pipe.passed and self.bird.rect.right > pipe.rect.right:
                    pipe.passed = True
                    self.score += 1

            if self.game_over:
                self.show_game_over()
                break

            self.screen.fill((135, 206, 250))
            for pipe in self.pipes:
                self.screen.blit(pipe.image, pipe.rect)
            self.screen.blit(self.bird.image, self.bird.rect)
            self.display_score()

            self.pipes = {pipe for pipe in self.pipes if pipe.rect.right >= 0}

            pygame.display.flip()
            self.clock.tick(30)

        return self.game_over

    def display_score(self):
        score_surface = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def show_game_over(self):
        game_over_surface = self.font.render('Game Over!', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(game_over_surface, game_over_rect)
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

