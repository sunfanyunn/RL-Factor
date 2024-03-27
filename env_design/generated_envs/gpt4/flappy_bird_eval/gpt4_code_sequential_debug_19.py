import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 5
GRAVITY = 0.5
BIRD_JUMP = -10
BIRD_WIDTH = 40
BIRD_HEIGHT = 40


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
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top):
        super().__init__()
        height = random.randint(150, SCREEN_HEIGHT - PIPE_GAP - 150)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, 0)) if is_top else self.image.get_rect(bottomleft=(x, SCREEN_HEIGHT))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.Font(None, 36)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.spawn_pipe()

    def spawn_pipe(self):
        top_pipe = Pipe(SCREEN_WIDTH, True)
        bottom_pipe = Pipe(SCREEN_WIDTH, False)
        bottom_pipe.rect.top = top_pipe.rect.bottom + PIPE_GAP
        self.pipes.add(top_pipe, bottom_pipe)

    def run(self, event):
        if not self.game_over:
            self.handle_events(event)
            self.process_game_logic()
            self.check_collisions()
            self.update_score_and_spawn_pipes()

        self.draw_game_elements()
        self.clock.tick(30)
        return not self.game_over

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.game_over = True
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
            self.bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.jump()

    def process_game_logic(self):
        self.bird.update()
        self.pipes.update()

    def draw_game_elements(self):
        self.screen.fill((135, 206, 235))
        self.screen.blit(self.bird.image, self.bird.rect)
        for pipe in self.pipes:
            self.screen.blit(pipe.image, pipe.rect)
        if self.game_over:
            self.show_game_over()
        else:
            self.display_score()
        pygame.display.flip()

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.pipes, False):
            self.game_over = True

        if self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

    def update_score_and_spawn_pipes(self):
        for pipe in self.pipes:
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                pipe.passed = True
                self.score += 0.5
                if self.score % 1 == 0:
                    self.spawn_pipe()

    def display_score(self):
        score_text = self.font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()


