import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_VELOCITY = -5
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
GRAVITY = 0.5
FLAP_STRENGTH = -10
BIRD_X_POSITION = SCREEN_WIDTH // 4


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # Yellow
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.velocity = 0
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

    def flap(self):
        self.velocity = FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top):
        super().__init__()
        height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))  # Green
        self.passed = False
        if is_top:
            self.rect = self.image.get_rect(bottomleft=(x, 0))
        else:
            self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT - height))

    def update(self):
        self.rect.x += PIPE_VELOCITY
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(BIRD_X_POSITION, SCREEN_HEIGHT // 2)
        self.bird_group = pygame.sprite.Group(self.bird)
        self.pipes = pygame.sprite.Group()
        self.spawn_new_pipe()
        self.pipe_frequency = 1500  # The frequency in milliseconds
        self.last_pipe_spawn = pygame.time.get_ticks()

    def spawn_new_pipe(self):
        x = SCREEN_WIDTH + PIPE_WIDTH
        self.pipes.add(Pipe(x, True))
        self.pipes.add(Pipe(x, False))

    def run(self, event):
        if self.game_over:
            # Insert game over logic here if needed
            return True

        # Process input
        if event and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                self.bird.flap()
            elif event.key == pygame.K_r:
                self.reset_game()

        # Update game state
        self.bird_group.update()
        self.pipes.update()

        # Handle collisions
        if pygame.sprite.spritecollide(self.bird, self.pipes, False):
            self.game_over = True

        # Check for bird hitting the ground
        if self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

        # Scoring
        for pipe in self.pipes:
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                pipe.passed = True
                self.score += 1

        # Pipe generation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_spawn > self.pipe_frequency:
            self.last_pipe_spawn = current_time
            self.spawn_new_pipe()

        # Drawing
        self.screen.fill((135, 206, 235))  # Clear the screen
        self.bird_group.draw(self.screen)
        self.pipes.draw(self.screen)

        # Draw the score
        font = pygame.font.Font(None, 36)
        score_surface = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_surface, (10, 10))

        # If game over, draw the game over
        if self.game_over:
            self.handle_game_over()

        pygame.display.flip()
        self.clock.tick(60)

        return not self.game_over

    def handle_game_over(self):
        font = pygame.font.Font(None, 72)
        game_over_surface = font.render('Game Over!', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        running = game.run(event)
    pygame.quit()
