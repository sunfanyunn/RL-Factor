import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP_SIZE = 200
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_SPEED = 5
GRAVITY = 1
FLAP_STRENGTH = 15


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY  # applying gravity
        self.rect.y += self.velocity

        # preventing bird from going out of the screen and above
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def flap(self):
        self.velocity = -FLAP_STRENGTH  # bird will move upwards


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_upper):
        super().__init__()
        height = random.randint(50, PIPE_HEIGHT)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))  # Green color

        # setting the position of the pipes
        if is_upper:
            y_pos = 0
            self.rect = self.image.get_rect(topright=(x, y_pos))
        else:
            y_gap = random.randint(PIPE_GAP_SIZE, SCREEN_HEIGHT - height - PIPE_GAP_SIZE)
            y_pos = y_gap + height
            self.rect = self.image.get_rect(bottomleft=(x, y_pos))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:  # if pipe is no longer visible
            self.kill()  # remove pipe


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group([self.bird])
        self.add_pipe_pair(SCREEN_WIDTH + PIPE_WIDTH)

    def add_pipe_pair(self, x):
        # creating a pair of pipes
        gap_y = random.randint(PIPE_GAP_SIZE, SCREEN_HEIGHT - PIPE_GAP_SIZE)
        upper_pipe = Pipe(x, True)
        lower_pipe = Pipe(x, False)
        upper_pipe.rect.bottom = gap_y - PIPE_GAP_SIZE // 2
        lower_pipe.rect.top = gap_y + PIPE_GAP_SIZE // 2
        self.pipes.add(upper_pipe, lower_pipe)
        self.all_sprites.add(upper_pipe, lower_pipe)

    def check_collision(self):
        # game over conditions
        if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

    def update_score(self):
        # updating score
        for pipe in self.pipes:
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                pipe.passed = True
                self.score += 1

    def run(self, event):
        # game loop
        if not self.game_over:
            self.all_sprites.update()
            self.check_collision()
            self.update_score()
            self.add_pipe_pair_if_needed()

        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird.flap()

        self.screen.fill((135, 206, 235))  # Light blue background
        self.all_sprites.draw(self.screen)

        score_surface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

        if self.game_over:
            self.display_game_over()

        pygame.display.flip()
        return True

    def add_pipe_pair_if_needed(self):
        # adding new pipes when needed
        last_pipe = self.pipes.sprites()[-1].rect if self.pipes else None
        if not last_pipe or last_pipe.right < SCREEN_WIDTH - 300:
            self.add_pipe_pair(SCREEN_WIDTH)

    def display_game_over(self):
        # displaying game over
        font = pygame.font.SysFont('Arial', 72)
        text_surface = font.render('Game Over!', True, (255, 0, 0))
        text_position = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_position.topleft)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

