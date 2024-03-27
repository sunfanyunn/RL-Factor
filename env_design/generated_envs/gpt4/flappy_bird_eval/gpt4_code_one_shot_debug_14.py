import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_MOVEMENT_SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = 20
BIRD_WIDTH = 50
BIRD_HEIGHT = 50


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            pygame.quit()
            sys.exit()

    def jump(self):
        self.velocity = -JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_bottom):
        super().__init__()
        height = random.randint(150, SCREEN_HEIGHT // 2)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect()
        self.rect.x = x
        if is_bottom:
            self.rect.top = y + PIPE_GAP
        else:
            self.rect.bottom = y
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVEMENT_SPEED
        if self.rect.right < 0:
            self.kill()


class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.bird)
        self.add_pipe_pair()

    def add_pipe_pair(self):
        y_position = random.randint(PIPE_GAP, SCREEN_HEIGHT - PIPE_GAP)
        top_pipe = Pipe(SCREEN_WIDTH, y_position, False)
        bottom_pipe = Pipe(SCREEN_WIDTH, y_position, True)
        self.pipes.add(top_pipe)
        self.pipes.add(bottom_pipe)
        self.all_sprites.add(top_pipe)
        self.all_sprites.add(bottom_pipe)

    def run(self, event):
        if self.game_over:
            self.display_game_over()
            return False

        self.handle_events(event)
        self.update_sprites()
        self.check_collisions()
        self.draw_game()

        if len(self.pipes) < 2:
            self.add_pipe_pair()

        self.clock.tick(60)

        return not self.game_over

    def handle_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (event.type == pygame.MOUSEBUTTONDOWN):
                self.bird.jump()

    def update_sprites(self):
        self.all_sprites.update()
        for pipe in self.pipes:
            if pipe.rect.centerx < self.bird.rect.left and not pipe.passed:
                self.score += 1
                pipe.passed = True

    def check_collisions(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.rect):
                self.game_over = True

    def draw_game(self):
        self.screen.fill((135, 206, 235))
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def display_game_over(self):
        over_text = self.font.render('Game Over!', True, (255, 255, 255))
        self.screen.blit(over_text, ((SCREEN_WIDTH - over_text.get_width()) // 2, (SCREEN_HEIGHT - over_text.get_height()) // 2))
        pygame.display.flip()
        pygame.time.wait(5000)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
