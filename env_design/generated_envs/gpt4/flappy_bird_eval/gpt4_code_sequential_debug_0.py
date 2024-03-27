import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 5
PIPE_ADD_INTERVAL = 1600
FLAP_STRENGTH = -10
GRAVITY = 0.5
BIRD_WIDTH = 34
BIRD_HEIGHT = 24


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
        elif self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height, inverted=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))  # green color
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.bottomleft = (x, 0)
        else:
            self.rect.topleft = (x, SCREEN_HEIGHT - height)
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED

    def is_off_screen(self):
        return self.rect.right < 0


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.background_color = (135, 206, 235)  # sky blue
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
    
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.time_since_last_pipe = PIPE_ADD_INTERVAL
    
    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game_over:
                self.reset_game()
            else:
                self.bird.flap()

        if not self.game_over:
            self.bird.update()
            self.pipes.update()

            for pipe in list(self.pipes):
                if pipe.is_off_screen():
                    self.pipes.remove(pipe)
                elif not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    self.score += 1
                    pipe.passed = True

            self.time_since_last_pipe += self.clock.get_time()
            if self.time_since_last_pipe >= PIPE_ADD_INTERVAL:
                self.add_pipe_pair()
                self.time_since_last_pipe = 0

            self.screen.fill(self.background_color)
            self.pipes.draw(self.screen)
            self.screen.blit(self.bird.image, self.bird.rect)

            score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_surface, (10, 10))

            self.check_collisions()

            pygame.display.flip()
            self.clock.tick(60)
        else:
            self.display_game_over()

        return True
    
    def add_pipe_pair(self):
        pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        top_pipe = Pipe(SCREEN_WIDTH, pipe_height, inverted=True)
        bottom_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT - pipe_height - PIPE_GAP)
        self.pipes.add(top_pipe)
        self.pipes.add(bottom_pipe)

    def check_collisions(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect):
                self.game_over = True
                break
        if self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

    def display_game_over(self):
        game_over_surface = self.font.render(f'Game Over! Score: {self.score}', True, (255, 69, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)  # run the game with the current event
    pygame.quit()
    sys.exit()
