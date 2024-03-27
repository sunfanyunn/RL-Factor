import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 3
BIRD_SIZE = 30
GRAVITY = 0.5
JUMP_STRENGTH = 10
PIPE_SPAWN_INTERVAL = 1500

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
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        if self.rect.top > 0:
            self.velocity = -JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, position):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        total_gap_height = SCREEN_HEIGHT - PIPE_GAP
        gap_top = random.randint(10, total_gap_height)
        if position == 'top':
            self.image.fill(GREEN)
            self.rect = self.image.get_rect(topleft=(x, gap_top - SCREEN_HEIGHT))
        else:
            self.image.fill(GREEN)
            self.rect = self.image.get_rect(topleft=(x, gap_top + PIPE_GAP))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.pipe_timer = pygame.time.get_ticks()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird.jump()

        if not self.game_over:
            if pygame.time.get_ticks() - self.pipe_timer > PIPE_SPAWN_INTERVAL:
                pipe_top = Pipe(SCREEN_WIDTH, 'top')
                pipe_bottom = Pipe(SCREEN_WIDTH, 'bottom')
                self.all_sprites.add(pipe_top, pipe_bottom)
                self.pipes.add(pipe_top, pipe_bottom)
                self.pipe_timer = pygame.time.get_ticks()

            self.all_sprites.update()
            self.screen.fill(WHITE)

            if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True

            for pipe in self.pipes:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    self.score += 1
                    pipe.passed = True

            self.all_sprites.draw(self.screen)

            if self.game_over:
                font = pygame.font.SysFont(None, 48)
                msg = font.render('Game Over!', True, BLACK)
                msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(msg, msg_rect)
            else:
                font = pygame.font.SysFont(None, 24)
                score_text = font.render(f'Score: {self.score}', True, BLACK)
                self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(30)

        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
