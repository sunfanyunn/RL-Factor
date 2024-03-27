import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 1
JUMP_HEIGHT = 20
PIPE_FREQUENCY = 1500  # in milliseconds
PIPE_GAP = 200
PIPE_SPEED = 5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))    # Yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

    def jump(self):
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, random.randint(100, SCREEN_HEIGHT // 2)))
        self.image.fill((0, 255, 0))    # Green color
        self.rect = self.image.get_rect()
        gap_center = random.randint(PIPE_GAP // 2, SCREEN_HEIGHT - PIPE_GAP // 2)
        if is_top:
            self.rect.bottomleft = (x, gap_center - PIPE_GAP // 2)
        else:
            self.rect.topleft = (x, gap_center + PIPE_GAP // 2)
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
        self.reset_game()
        self.font = pygame.font.Font(None, 70)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.spawn_pipe_pair()
        self.last_pipe_time = pygame.time.get_ticks()

    def spawn_pipe_pair(self):
        gap_center = random.randint(PIPE_GAP // 2, SCREEN_HEIGHT - PIPE_GAP // 2)
        top_pipe = Pipe(SCREEN_WIDTH, True)
        bottom_pipe = Pipe(SCREEN_WIDTH, False)
        self.pipes.add(top_pipe, bottom_pipe)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if not self.game_over and (event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP] or event.type == pygame.MOUSEBUTTONDOWN):
            self.bird.jump()

        now = pygame.time.get_ticks()
        if not self.game_over and now - self.last_pipe_time > PIPE_FREQUENCY:
            self.last_pipe_time = now
            self.spawn_pipe_pair()

        self.bird.update()
        self.pipes.update()

        if pygame.sprite.spritecollideany(self.bird, self.pipes):
            self.game_over = True

        if not self.game_over:
            for pipe in self.pipes:
                if not pipe.passed and self.bird.rect.right > pipe.rect.left and pipe.rect.right < SCREEN_WIDTH:
                    pipe.passed = True
                    self.score += 1
            self.screen.fill((135, 206, 250))  # Background color
            self.pipes.draw(self.screen)
            self.screen.blit(self.bird.image, self.bird.rect)
            self.display_score()
        else:
            self.show_game_over()

        pygame.display.flip()
        self.clock.tick(30)

        return True

    def display_score(self):
        score_surface = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def show_game_over(self):
        game_over_surface = self.font.render('Game Over!', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

