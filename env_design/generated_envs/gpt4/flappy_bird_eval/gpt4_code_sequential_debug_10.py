import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200
PIPE_MOVEMENT_SPEED = 5
BIRD_X = 100
BIRD_Y = SCREEN_HEIGHT // 2
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_ADD_INTERVAL = 1500


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity = 0
            self.rect.bottom = SCREEN_HEIGHT

    def jump(self):
        self.velocity = JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_bottom, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 128, 0))
        if is_bottom:
            self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT - height))
        else:
            self.rect = self.image.get_rect(bottomleft=(x, height + PIPE_GAP))
        self.x = x
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVEMENT_SPEED
        if self.rect.right < 0:
            self.kill()


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(BIRD_X, BIRD_Y)
        self.bird_group = pygame.sprite.GroupSingle(self.bird)
        self.pipe_group = pygame.sprite.Group()
        self.last_pipe_time = pygame.time.get_ticks()
        self.add_pipe()

    def add_pipe(self):
        x = SCREEN_WIDTH
        height = random.randint(50, PIPE_HEIGHT - PIPE_GAP)
        self.pipe_group.add(Pipe(x, False, height), Pipe(x, True, PIPE_HEIGHT - height))

    def run(self, event):
        if not self.game_over:
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP]:
                self.bird.jump()

            self.bird_group.update()

            time_now = pygame.time.get_ticks()
            if time_now - self.last_pipe_time > PIPE_ADD_INTERVAL:
                self.add_pipe()
                self.last_pipe_time = time_now

            self.pipe_group.update()
            for pipe in self.pipe_group:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 1

            self.screen.fill((135, 206, 250))
            self.bird_group.draw(self.screen)
            self.pipe_group.draw(self.screen)

            if pygame.sprite.spritecollide(self.bird, self.pipe_group, False):
                self.game_over = True

            score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)
        else:
            game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            pygame.display.flip()

        return not self.game_over

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()

