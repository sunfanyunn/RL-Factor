import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP_SIZE = 200
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
GRAVITY = 0.25
JUMP_STRENGTH = -10
PIPE_MOVEMENT_SPEED = 3


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, position):
        super().__init__()
        height = random.randint(50, PIPE_HEIGHT)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        if position == 'top':
            self.rect = self.image.get_rect(bottomleft=(x, SCREEN_HEIGHT / 2 - PIPE_GAP_SIZE / 2))
        else:
            self.rect = self.image.get_rect(topleft=(x, SCREEN_HEIGHT / 2 + PIPE_GAP_SIZE / 2))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVEMENT_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.bird_group = pygame.sprite.GroupSingle()
        self.pipes = pygame.sprite.Group()
        self.reset_game()
        
    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(150, SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)
        self.pipes.empty()
        self.add_pipe()
        
    def run(self, event):
        if self.game_over:
            self.display_game_over()
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                self.bird.jump()

        self.bird_group.update()
        self.pipes.update()
        self.screen.fill((255, 255, 255))
        self.bird_group.draw(self.screen)
        self.pipes.draw(self.screen)

        if pygame.sprite.spritecollide(self.bird, self.pipes, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

        for pipe in self.pipes:
            if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                pipe.passed = True
                self.score += 1
                self.add_pipe()

        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(30)
        return True

    def add_pipe(self):
        pipe_x_position = SCREEN_WIDTH + PIPE_WIDTH
        self.pipes.add(Pipe(pipe_x_position, 'top'))
        self.pipes.add(Pipe(pipe_x_position, 'bottom'))

    def display_game_over(self):
        text = self.font.render('Game Over!', True, (255, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
