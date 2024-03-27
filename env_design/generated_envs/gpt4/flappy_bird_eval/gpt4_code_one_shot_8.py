import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
PIPE_WIDTH = 80
BIRD_SIZE = 30
GRAVITY = 0.25
JUMP_STRENGTH = 5
PIPE_GAP = 200
PIPE_SPEED = 3
PIPE_SPAWN_INTERVAL = 1800

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0

    def update(self):
        self.vel += GRAVITY
        self.rect.y += self.vel
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel = 0

    def jump(self):
        self.vel = -JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, pipe_position):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill(GREEN)
        total_gap_height = SCREEN_HEIGHT - PIPE_GAP
        pipe_height = random.randint(10, total_gap_height)
        offset = pipe_height + PIPE_GAP if pipe_position == 'top' else 0
        self.rect = self.image.get_rect(topleft=(x, -SCREEN_HEIGHT + offset if pipe_position == 'top' else offset))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.bird_group = pygame.sprite.GroupSingle(self.bird)
        self.score = 0
        self.game_over = False
        self.pipe_timer = pygame.time.get_ticks()

    def run(self, event):
        while not self.game_over:
            self.screen.fill(WHITE)
            if event.type == pygame.QUIT:
                self.game_over = True

            # Bird movement
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN) and self.bird.rect.bottom < SCREEN_HEIGHT:
                self.bird.jump()

            # Pipes spawning
            current_time = pygame.time.get_ticks()
            if current_time - self.pipe_timer > PIPE_SPAWN_INTERVAL:
                pipe_top = Pipe(SCREEN_WIDTH, 'top')
                pipe_bottom = Pipe(SCREEN_WIDTH, 'bottom')
                self.pipe_timer = current_time
                self.pipes.add(pipe_top)
                self.pipes.add(pipe_bottom)

            # Pipes movement and scoring
            for pipe in list(self.pipes):
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    self.score += 1
                    pipe.passed = True
                if pipe.rect.right <= 0:
                    self.pipes.remove(pipe)

            # Collision Check
            if pygame.sprite.spritecollide(self.bird, self.pipes, False):
                self.game_over = True

            self.bird_group.update()
            self.pipes.update()

            self.bird_group.draw(self.screen)
            self.pipes.draw(self.screen)

            # Score Display
            font = pygame.font.SysFont(None, 24)
            img = font.render(f'Score: {self.score}', True, BLACK)
            self.screen.blit(img, (10, 10))

            if self.game_over:
                font = pygame.font.SysFont(None, 48)
                msg = font.render('Game Over!', True, BLACK)
                msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(msg, msg_rect)

            pygame.display.flip()
            self.clock.tick(120)

            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                self.game_over = True

        return False

if __name__ == "__main__":
    game = Game()
    game.run(pygame.event.poll())
    pygame.quit()
