import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PIPE_WIDTH = 80
PIPE_GAP = 200
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
GRAVITY = 0.5
JUMP_HEIGHT = 10
PIPE_MOVEMENT = -5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # Yellow bird
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top=False):
        super().__init__()
        height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))  # Green pipes
        if is_top:
            self.rect = self.image.get_rect(bottomleft=(x, 0))
        else:
            self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT - height))
        self.passed = False

    def update(self):
        self.rect.x += PIPE_MOVEMENT
        if self.rect.right < 0:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
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
        self.bird = Bird(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
        self.bird_group.add(self.bird)
        self.spawn_pipe()

    def spawn_pipe(self):
        x_pos = SCREEN_WIDTH + 100
        self.pipe_group.add(Pipe(x_pos, is_top=True))
        self.pipe_group.add(Pipe(x_pos, is_top=False))

    def run(self, event):
        self.screen.fill((135, 206, 250))  # Light blue background
        if not self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.bird.jump()

            self.bird_group.update()
            self.pipe_group.update()

            self.bird_group.draw(self.screen)
            self.pipe_group.draw(self.screen)

            # Check for collisions
            if pygame.sprite.spritecollide(self.bird, self.pipe_group, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True

            # Check if pipe has been passed
            for pipe in self.pipe_group:
                if self.bird.rect.centerx > pipe.rect.right and not pipe.passed:
                    self.score += 1
                    pipe.passed = True

            self.spawn_new_pipe_if_required()

        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))

        pygame.display.flip()
        self.clock.tick(60)

        return not self.game_over

    def spawn_new_pipe_if_required(self):
        if not any(pipe.rect.centerx > SCREEN_WIDTH/2 for pipe in self.pipe_group):
            self.spawn_pipe()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            running &= game.run(event)
    pygame.quit()
