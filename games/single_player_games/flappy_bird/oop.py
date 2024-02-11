import pygame
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BIRD_SIZE = 32
PIPE_WIDTH = 80
PIPE_GAP = 200
SPEED = 5
GRAVITY = 0.5
FLAP = -12
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1

    def update(self):
        self.speed += GRAVITY
        self.rect.y += self.speed

    def flap(self):
        self.speed = FLAP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.gap_start = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.rect(self.image, GREEN, (0, 0, PIPE_WIDTH, self.gap_start))
        pygame.draw.rect(
            self.image, GREEN, (0, self.gap_start + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT)
        )
        self.rect = self.image.get_rect(topleft=(self.x, 0))
        self.passed = False

    def update(self):
        self.rect.x -= SPEED

    def collides_with(self, bird):
        if bird.rect.colliderect(
            pygame.Rect(self.rect.x, 0, PIPE_WIDTH, self.gap_start)
        ):
            return True
        if bird.rect.colliderect(
            pygame.Rect(
                self.rect.x, self.gap_start + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT
            )
        ):
            return True

        return False


class Game:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.grid_size = None
        self.fps = 60
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "gray": (100, 100, 100),
        }
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.bird = Bird(self.width // 4, self.height // 2) # Pass the game instance
        self.pipes = []
        pipe = Pipe(self.width)
        self.pipes.append(pipe)
        self.game_over = False
        self.score = 0
        self.restart_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2, 140, 40
        )

    def run(self, event):
        # return false if you want to quit the game
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_over and self.restart_button.collidepoint(
                pygame.mouse.get_pos()
            ):
                self.reset_game()
            elif not self.game_over:
                self.bird.flap()

        if not self.game_over:
            self.bird.update()
            for pipe in self.pipes:
                pipe.update()

            # Check if the bird hits the top or bottom of the screen
            if self.bird.rect.y <= 0 or self.bird.rect.y + BIRD_SIZE >= SCREEN_HEIGHT:
                self.game_over = True

            for pipe in self.pipes:
                if not pipe.passed and pipe.rect.x < self.bird.rect.x:
                    self.score += 1
                    pipe.passed = True

                if pipe.collides_with(self.bird):
                    self.game_over = True

        self.screen.fill(WHITE)
        self.screen.blit(self.bird.image, self.bird.rect)
        for pipe in self.pipes:
            self.screen.blit(pipe.image, pipe.rect)


        font = pygame.font.SysFont(None, 36)
        score_text = font.render(str(self.score), True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            font = pygame.font.SysFont(None, 50)
            text = font.render("Game Over!", True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
            )
            self.screen.blit(text, text_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), self.restart_button)
            restart_text = font.render("Restart", True, WHITE)
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            )
            self.screen.blit(restart_text, restart_rect)
        else:
            old_pipes = self.pipes.copy()
            self.pipes = []
            for pipe in old_pipes:
                if pipe.rect.x + PIPE_WIDTH < 0:
                    pipe.kill()
                    new_pipe = Pipe(SCREEN_WIDTH)
                    self.pipes.append(new_pipe)
                else:
                    self.pipes.append(pipe)


        pygame.display.flip()
        self.clock.tick(self.fps)
        return True


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()