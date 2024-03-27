import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_WIDTH = 80
PIPE_SPACING = 200
PIPE_GAP = 200
GRAVITY = 1
JUMP_STRENGTH = 12
PIPE_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY  # Apply gravity to velocity
        self.rect.y += self.velocity  # Apply velocity to bird's position
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_STRENGTH  # negative velocity to move upwards


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, upper=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect()
        if upper:
            self.rect.bottom = self.rect.height - PIPE_SPACING
        else:
            self.rect.top = SCREEN_HEIGHT - self.rect.height + PIPE_SPACING
        self.rect.x = x
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.SysFont(None, 40)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.pipes.append(Pipe(SCREEN_WIDTH))
        self.pipes.append(Pipe(SCREEN_WIDTH, upper=True))
        self.all_sprites = pygame.sprite.Group(self.bird, *self.pipes)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if not self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP)):
                self.bird.jump()

            self.screen.fill((135, 206, 250))  # Sky blue background
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.score_text = self.font.render(str(self.score), True, (0, 0, 0))
            self.screen.blit(self.score_text, (10, 10))

            # Collision detection
            if pygame.sprite.spritecollideany(self.bird, self.pipes):
                self.game_over = True
            if self.bird.rect.bottom > SCREEN_HEIGHT:
                self.game_over = True

            # Check if pipes need to be removed or counted for score
            for pipe in self.pipes[:]:
                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)
                    self.all_sprites.remove(pipe)
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 0.5  # Increment by 0.5 because there are two pipes

            # Add new pipes when needed
            if not self.pipes or self.pipes[-1].rect.x < SCREEN_WIDTH - PIPE_SPACING:
                self.pipes.append(Pipe(SCREEN_WIDTH))
                self.pipes.append(Pipe(SCREEN_WIDTH, upper=True))
                for pipe in self.pipes[-2:]:
                    self.all_sprites.add(pipe)

            self.clock.tick(30)

        else:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        pygame.display.flip()
        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()