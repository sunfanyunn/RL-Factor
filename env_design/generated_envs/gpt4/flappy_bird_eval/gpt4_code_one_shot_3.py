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
GRAVITY = 1
JUMP_HEIGHT = 20
PIPE_SPEED = 5
PIPE_SPAWN_FREQUENCY = 75


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.surf.fill((255, 255, 0))
        self.rect = self.surf.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.velocity = 0
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, orientation, height):
        super().__init__()
        self.surf = pygame.Surface((PIPE_WIDTH, height))
        self.surf.fill((0, 128, 0))
        if orientation == 'top':
            self.rect = self.surf.get_rect(topright=(x, 0))
        elif orientation == 'bottom':
            self.rect = self.surf.get_rect(bottomright=(x, SCREEN_HEIGHT))
        self.passed = False
        self.orientation = orientation

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.font = pygame.font.Font(None, 64)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.pipe_frequency = PIPE_SPAWN_FREQUENCY
        self.frame_count = 0

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.bird.jump()

            self.screen.fill((135, 206, 250))
            self.all_sprites.update()

            if self.frame_count % self.pipe_frequency == 0:
                height = random.randint(100, 300)
                top_pipe = Pipe(SCREEN_WIDTH + PIPE_WIDTH, 'top', height)
                bottom_pipe = Pipe(SCREEN_WIDTH + PIPE_WIDTH, 'bottom', SCREEN_HEIGHT - height - PIPE_GAP)
                self.pipes.add(top_pipe, bottom_pipe)
                self.all_sprites.add(top_pipe, bottom_pipe)

            for pipe in self.pipes:
                if pipe.rect.right < self.bird.rect.left and not pipe.passed:
                    pipe.passed = True
                    self.score += 0.5

            self.pipes.update()
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            if pygame.sprite.spritecollideany(self.bird, self.pipes):
                self.game_over = True

            self.display_score()

            self.frame_count += 1
        else:
            self.display_game_over()

        pygame.display.flip()
        self.clock.tick(30)
        return True

    def display_score(self):
        score_text = self.font.render('Score: {}'.format(int(self.score)), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
