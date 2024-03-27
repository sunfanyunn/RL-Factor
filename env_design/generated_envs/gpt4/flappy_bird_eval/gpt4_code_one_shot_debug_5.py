import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_INTERVAL = 1600 # milliseconds
PIPE_SPEED = 3
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
GRAVITY = 0.5
JUMP_STRENGTH = -10
BIRD_X_POSITION = SCREEN_WIDTH // 3
PIPE_GENERATION_EVENT = pygame.USEREVENT + 1


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity_y = 0

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += int(self.velocity_y)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0

    def jump(self):
        self.velocity_y = JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_upper, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        if is_upper:
            self.rect.bottomleft = (x, 0)
        else:
            self.rect.topright = (x, SCREEN_HEIGHT)
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
        self.font = pygame.font.SysFont('Arial', 30, True)
        self.reset_game()
        pygame.time.set_timer(PIPE_GENERATION_EVENT, PIPE_INTERVAL)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(BIRD_X_POSITION, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.bird)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == PIPE_GENERATION_EVENT:
            self.spawn_pipes()
        if not self.game_over and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN):
            self.bird.jump()

        if not self.game_over:
            self.all_sprites.update()
            self.pipes.update()
            self.screen.fill((135, 206, 250))
            self.all_sprites.draw(self.screen)
            self.pipes.draw(self.screen)

            self.check_collisions()

            score_text = self.font.render(f'Score: {int(self.score)}', True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))
        else:
            self.show_game_over()

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def spawn_pipes(self):
        top_pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        top_pipe = Pipe(SCREEN_WIDTH, True, top_pipe_height)
        bottom_pipe = Pipe(SCREEN_WIDTH, False, SCREEN_HEIGHT - top_pipe_height - PIPE_GAP)
        self.pipes.add(top_pipe)
        self.pipes.add(bottom_pipe)

    def check_collisions(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect):
                self.game_over = True
            if pipe.rect.right < self.bird.rect.left and not pipe.passed:
                pipe.passed = True
                self.score += 0.5
        if self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

    def show_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type != pygame.NOEVENT:
            running = game.run(event)
    pygame.quit()
    sys.exit()
