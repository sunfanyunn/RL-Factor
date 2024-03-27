import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_FREQUENCY = 1500  # milliseconds
PIPE_SPEED = 5
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_JUMP = -15
GRAVITY = 1


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

    def jump(self):
        self.velocity = BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, upper=False):
        super().__init__()
        bottom = random.randint(PIPE_GAP // 2, SCREEN_HEIGHT - PIPE_GAP)
        height = SCREEN_HEIGHT - bottom if upper else bottom - PIPE_GAP // 2
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        top = 0 if upper else SCREEN_HEIGHT - height
        self.rect = self.image.get_rect(topleft=(x, top))
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
        self.bird_group = pygame.sprite.GroupSingle()
        self.pipe_group = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        pygame.time.set_timer(pygame.USEREVENT + 1, PIPE_FREQUENCY)

    def reset_game(self):
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)
        self.game_over = False
        self.score = 0

    def add_pipe(self):
        x = SCREEN_WIDTH + PIPE_WIDTH
        self.pipe_group.add(Pipe(x, upper=True))
        self.pipe_group.add(Pipe(x, upper=False))

    def run(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key in {pygame.K_SPACE, pygame.K_UP}:
            if not self.game_over:
                self.bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.game_over:
                self.bird.jump()
        elif event.type == pygame.USEREVENT + 1:
            self.add_pipe()

        if not self.game_over:
            self.bird_group.update()
            self.pipe_group.update()
            if pygame.sprite.spritecollide(self.bird, self.pipe_group, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
                self.game_over = True
            for pipe in self.pipe_group:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    self.score += 1
                    pipe.passed = True

        self.screen.fill((135, 206, 250))
        self.bird_group.draw(self.screen)
        self.pipe_group.draw(self.screen)
        self.display_score()
        if self.game_over:
            self.display_game_over()
        pygame.display.flip()
        self.clock.tick(30)
        return not self.game_over

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
        self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()