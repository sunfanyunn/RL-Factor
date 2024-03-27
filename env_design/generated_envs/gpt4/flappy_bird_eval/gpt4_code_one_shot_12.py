import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
GRAVITY = 1
JUMP_STRENGTH = 20
PIPE_GAP_SIZE = 200
PIPE_MOVEMENT_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, BIRD_WIDTH, BIRD_HEIGHT)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.y > SCREEN_HEIGHT - BIRD_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - BIRD_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, rect):
        super().__init__()
        self.rect = rect
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVEMENT_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipe_group = pygame.sprite.Group()
        self.spawn_pipe()

    def spawn_pipe(self):
        gap_start = random.randint(50, SCREEN_HEIGHT - 50 - PIPE_GAP_SIZE)
        bottom_rect = pygame.Rect(SCREEN_WIDTH, gap_start + PIPE_GAP_SIZE, PIPE_WIDTH, SCREEN_HEIGHT)
        top_rect = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, gap_start)
        self.pipe_group.add(Pipe(SCREEN_WIDTH, top_rect), Pipe(SCREEN_WIDTH, bottom_rect))

    def check_collision(self):
        if pygame.sprite.spritecollideany(self.bird, self.pipe_group) or self.bird.rect.y >= SCREEN_HEIGHT - BIRD_HEIGHT:
            self.game_over = True

    def run(self, event):
        if self.game_over:
            return False
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.jump()

        self.screen.fill((255, 255, 255))
        self.bird.update()
        self.pipe_group.update()

        for pipe in self.pipe_group:
            pygame.draw.rect(self.screen, (0, 255, 0), pipe.rect)
            if pipe.rect.right < 0:
                self.pipe_group.remove(pipe)
            elif not pipe.passed and pipe.rect.right < self.bird.rect.left:
                pipe.passed = True
                self.score += 0.5  # Increment by 0.5 because two pipes are passed (top and bottom)

        pygame.draw.rect(self.screen, (255, 0, 0), self.bird.rect)

        self.check_collision()

        if self.game_over:
            font = pygame.font.SysFont(None, 74)
            text = font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return False

        font = pygame.font.SysFont(None, 36)
        score_text = font.render('Score: ' + str(int(self.score)), True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        if len(self.pipe_group) < 4:  # spares the next set of pipes
            self.spawn_pipe()

        pygame.display.flip()
        self.clock.tick(30)
        return True

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
