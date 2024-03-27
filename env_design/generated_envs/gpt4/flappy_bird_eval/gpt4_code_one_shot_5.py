import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PIPE_WIDTH = 80
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
GRAVITY = 0.5
JUMP_STRENGTH = -10
BIRD_X_POSITION = SCREEN_WIDTH // 3
PIPE_GAP = 200
PIPE_INTERVAL = 1600 # milliseconds
PIPE_SPEED = 3


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, BIRD_WIDTH, BIRD_HEIGHT)
        self.velocity_y = 0

    def jump(self):
        self.velocity_y = JUMP_STRENGTH

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += int(self.velocity_y)

        # Prevent bird from going out of the window
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT

        if self.rect.y < 0:
            self.rect.y = 0


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_upper, height):
        super().__init__()
        self.x = x
        self.passed = False

        if is_upper:
            self.rect = pygame.Rect(x, -PIPE_GAP // 2 + height, PIPE_WIDTH, SCREEN_HEIGHT // 2)
        else:
            self.rect = pygame.Rect(x, SCREEN_HEIGHT // 2 + PIPE_GAP // 2 + height, PIPE_WIDTH, SCREEN_HEIGHT)

    def update(self):
        self.x -= PIPE_SPEED
        self.rect.x = self.x


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.SysFont('Arial', 30, True)
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer, PIPE_INTERVAL)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(BIRD_X_POSITION, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)

    def run(self, event):
        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.game_over:
                self.bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.bird.jump()
            if event.type == self.pipe_timer:
                pipe_height = random.randint(-SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 4)
                bottom_pipe = Pipe(SCREEN_WIDTH, False, pipe_height)
                top_pipe = Pipe(SCREEN_WIDTH, True, pipe_height)
                self.pipes.add(bottom_pipe)
                self.pipes.add(top_pipe)
                self.all_sprites.add(bottom_pipe)
                self.all_sprites.add(top_pipe)

        # Game logic
        if not self.game_over:
            self.all_sprites.update()

            for pipe in self.pipes:
                if pipe.rect.x < self.bird.rect.x and not pipe.passed:
                    pipe.passed = True
                    self.score += 1
                
            for pipe in self.pipes:
                if self.bird.rect.colliderect(pipe.rect):
                    self.game_over = True
                    break

            if self.bird.rect.y >= SCREEN_HEIGHT - BIRD_HEIGHT:
                self.game_over = True

        # Drawing
        self.screen.fill((135, 206, 250))  # Sky blue background
        for entity in self.all_sprites:
            pygame.draw.rect(self.screen, (0, 255, 0) if isinstance(entity, Pipe) else (255, 0, 0), entity.rect)

        # Draw the score on the screen
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        # Update screen
        pygame.display.flip()

        # Maintain framerate
        self.clock.tick(60)

        return not self.game_over

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run(pygame.event.poll())
    pygame.quit()
