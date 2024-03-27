import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
PIPE_WIDTH = 80
PIPE_GAP = 200
GRAVITY = 0.5
JUMP_HEIGHT = 12
PIPE_SPEED = 5
PIPE_SPAWN_FREQUENCY = 75


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, orientation, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 128, 0))
        if orientation == 'top':
            self.rect = self.image.get_rect(midbottom=(x, 0))
        else:
            self.rect = self.image.get_rect(midtop=(x, SCREEN_HEIGHT))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 64)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
        self.bird_group = pygame.sprite.GroupSingle(self.bird)
        self.pipes = pygame.sprite.Group()
        self.frame_count = 0

    def run(self, event):
        if not self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jump()
            self.screen.fill((135, 206, 235))  # Sky blue background
            self.bird_group.update()
            self.pipes.update()

            # Check for collisions
            if pygame.sprite.spritecollide(self.bird, self.pipes, False):
                self.game_over = True

            # Spawn pipes
            self.frame_count += 1
            if self.frame_count >= PIPE_SPAWN_FREQUENCY:
                self.frame_count = 0
                pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
                top_pipe = Pipe(SCREEN_WIDTH, 'top', pipe_height)
                bottom_pipe = Pipe(SCREEN_WIDTH, 'bottom', SCREEN_HEIGHT - pipe_height - PIPE_GAP)
                self.pipes.add(top_pipe, bottom_pipe)

            # Remove passed pipes and increase score
            for pipe in self.pipes:
                if pipe.rect.right < self.bird.rect.left and not pipe.passed:
                    pipe.passed = True
                    self.score += 1

            # Draw everything
            self.pipes.draw(self.screen)
            self.bird_group.draw(self.screen)
            self.display_score()

            # End game if bird hits the ground
            if self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True
        else:
            self.display_game_over()

        pygame.display.flip()
        self.clock.tick(30)
        return True

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(game_over_text, game_over_rect)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
    pygame.quit()
