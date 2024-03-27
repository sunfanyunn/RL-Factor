import pygame
import random

# Initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = -5


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        if not game.game_over:
            self.velocity += GRAVITY
            self.rect.y += int(self.velocity)
            if self.rect.top < 0:
                self.rect.top = 0
                self.velocity = 0
            if self.rect.bottom > SCREEN_HEIGHT:
                game.game_over = True

    def flap(self):
        if not game.game_over:
            self.velocity = FLAP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.passed = False
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.set_colorkey((0, 0, 0))
        self.image.fill((0, 0, 0))
        top_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, top_height)
        self.bottom_rect = pygame.Rect(x, top_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - top_height - PIPE_GAP)
        pygame.draw.rect(self.image, (0, 255, 0), self.top_rect)
        pygame.draw.rect(self.image, (0, 255, 0), self.bottom_rect)
        self.rect = self.image.get_rect()

    def update(self):
        if not game.game_over:
            self.rect.x += PIPE_SPEED
            if self.rect.right < 0:
                self.kill()
            self.top_rect.x += PIPE_SPEED
            self.bottom_rect.x += PIPE_SPEED


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        pygame.display.set_caption('Flappy Bird Clone')
        self.reset_game()
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer, 1500)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        self.pipe_group = pygame.sprite.Group()
        self.pipe_group.add(Pipe(SCREEN_WIDTH))

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            self.bird.flap()
        if event.type == self.pipe_timer:
            pipe = Pipe(SCREEN_WIDTH)
            self.pipe_group.add(pipe)
            self.all_sprites.add(pipe)

        if not self.game_over:
            self.screen.fill((135, 206, 235))
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            pipe_passed = False
            for pipe in self.pipe_group:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe_passed = True
                    pipe.passed = True
            if pipe_passed:
                self.score += 1

            for pipe in self.pipe_group:
                if pipe.top_rect.colliderect(self.bird.rect) or pipe.bottom_rect.colliderect(self.bird.rect):
                    self.game_over = True

            score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            if self.game_over:
                game_over_text = self.font.render('Game Over!', True, (255, 0, 0))
                text_rect = game_over_text.get_rect()
                text_rect.center = self.screen.get_rect().center
                self.screen.blit(game_over_text, text_rect)
        else:
            return False

        self.clock.tick(60)
        pygame.display.flip()
        return True

if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if not game.run(event):
                running = False
        if running and game.game_over:
            game.reset_game()
    pygame.quit()
