import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_GAP = 200
PIPE_MOVEMENT_SPEED = 5
GRAVITY = 2
JUMP_STRENGTH = 20


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = 0

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Stay in screen bounds
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_bottom):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(100, 700)))
        self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT if is_bottom else -self.image.get_height()))
        self.image.fill((0, 255, 0))  # Green color
        self.speed = PIPE_MOVEMENT_SPEED
        self.passed = False

    def update(self):
        self.rect.x -= self.speed


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.Font(None, 74)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
        self.pipes = pygame.sprite.Group()

        # Add initial pipes
        self.add_pipe_pair()

    def add_pipe_pair(self):
        y_bottom = random.randint(SCREEN_HEIGHT//2, SCREEN_HEIGHT-PIPE_GAP)
        bottom_pipe = Pipe(SCREEN_WIDTH, True)
        bottom_pipe.rect.top = y_bottom + PIPE_GAP
        top_pipe = Pipe(SCREEN_WIDTH, False)
        top_pipe.rect.bottom = y_bottom

        self.pipes.add(top_pipe)
        self.pipes.add(bottom_pipe)

    def run(self, event):
        # Event Handling
        if event.type == pygame.QUIT:
            return False
        if not self.game_over and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.bird.jump()

        # Update game state
        if not self.game_over:
            self.bird.update()
            self.pipes.update()

            for pipe in self.pipes:
                # Check if the bird has passed the pipe
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 1

                # Game over if bird hits a pipe
                if self.bird.rect.colliderect(pipe.rect):
                    self.game_over = True

            # Game over if bird hits the ground
            if self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True

            # Remove off-screen pipes and add new ones
            if not self.pipes.sprites()[0].rect.colliderect(self.screen.get_rect()):
                self.pipes.sprites()[0].kill()
                self.pipes.sprites()[0].kill()
                self.add_pipe_pair()

        # Draw/update screen
        self.screen.fill((135, 206, 250))  # Fill the screen with a light blue color
        self.pipes.draw(self.screen)
        self.screen.blit(self.bird.image, self.bird.rect)

        # Show score
        score_text = self.font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Show game over message
        if self.game_over:
            over_text = self.font.render('Game Over!', True, (255, 255, 255))
            self.screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//2 - over_text.get_height()//2))

        pygame.display.flip()
        self.clock.tick(60)  # Maintain 60 FPS

        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
