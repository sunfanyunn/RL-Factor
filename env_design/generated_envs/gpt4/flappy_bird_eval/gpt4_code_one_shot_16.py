
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
PIPE_GAP = 200
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_MOVEMENT_X = -5
PIPE_SPAWN_FREQUENCY = 1500 # milliseconds


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
        self.velocity = JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_bottom):
        super().__init__()
        self.is_bottom = is_bottom
        height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))  # Green pipe

        if is_bottom:
            self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT - height))
        else:
            self.rect = self.image.get_rect(bottomleft=(x, SCREEN_HEIGHT - height - PIPE_GAP))

        self.passed = False

    def update(self):
        self.rect.x += PIPE_MOVEMENT_X


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        bird_x = SCREEN_WIDTH // 4
        bird_y = SCREEN_HEIGHT // 2
        self.bird = Bird(bird_x, bird_y)
        self.bird_group = pygame.sprite.GroupSingle(self.bird)
        self.pipes = pygame.sprite.Group()
        self.spawn_pipe()

        pygame.time.set_timer(pygame.USEREVENT, PIPE_SPAWN_FREQUENCY)

    def spawn_pipe(self):
        x = SCREEN_WIDTH + 100
        self.pipes.add(Pipe(x, False))
        self.pipes.add(Pipe(x, True))

    def run(self, event):
        if self.game_over:
            self.display_game_over()
            return False

        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.USEREVENT:
            self.spawn_pipe()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                self.bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.jump()

        self.bird_group.update()

        for pipe in self.pipes:
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                pipe.passed = True
                self.score += 1

        self.pipes.update()
        self.check_collisions()

        self.draw()

        self.clock.tick(30)
        return True

    def check_collisions(self):
        collided_pipe = pygame.sprite.spritecollideany(self.bird, self.pipes)
        if collided_pipe or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

    def display_game_over(self):
        text = self.font.render('Game Over!', True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def draw(self):
        self.screen.fill((135, 206, 250))  # Sky blue background
        self.pipes.draw(self.screen)
        self.bird_group.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
