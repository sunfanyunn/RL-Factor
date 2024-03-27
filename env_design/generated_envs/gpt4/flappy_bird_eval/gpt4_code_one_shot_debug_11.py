import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
GRAVITY = 1
BIRD_JUMP = 12
PIPE_GAP_SIZE = 200
PIPE_MOVE_SPEED = 5
PIPE_SPAWN_RATE = 1500  # milliseconds


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, width=34, height=24):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        if self.rect.top > 0:
            self.velocity = -BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_upper=False, height=400):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        y = SCREEN_HEIGHT - height if is_upper else 0
        self.rect = self.image.get_rect(topleft=(x, y))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.last_pipe_spawn_time = pygame.time.get_ticks()
        self.generate_pipe_pair()

    def generate_pipe_pair(self):
        pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP_SIZE - 50)
        self.pipes.add(Pipe(SCREEN_WIDTH, True, pipe_height))
        self.pipes.add(Pipe(SCREEN_WIDTH, False, SCREEN_HEIGHT - pipe_height - PIPE_GAP_SIZE))
        self.last_pipe_spawn_time = pygame.time.get_ticks()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP)) or (event.type == pygame.MOUSEBUTTONDOWN):
            self.bird.jump()

        self.screen.fill((135, 206, 250))
        if not self.game_over:
            self.bird.update()
            self.pipes.update()
            self.check_collisions()

            now = pygame.time.get_ticks()
            if now - self.last_pipe_spawn_time > PIPE_SPAWN_RATE:
                self.generate_pipe_pair()

            for pipe in self.pipes:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    self.score += 1
                    pipe.passed = True

        self.pipes.draw(self.screen)
        self.screen.blit(self.bird.image, self.bird.rect)

        score_surf = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))

        if self.game_over:
            self.show_game_over()

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def check_collisions(self):
        if pygame.sprite.spritecollideany(self.bird, self.pipes) or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

    def show_game_over(self):
        game_over_surf = self.font.render('Game Over!', True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surf, game_over_rect)

if __name__ == '\_\_main\_\_':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if not game.game_over:
                    game.bird.jump()

        if not game.game_over:
            game.screen.fill((135, 206, 250))
            game.bird.update()
            game.pipes.update()
            game.check_collisions()

            now = pygame.time.get_ticks()
            if now - game.last_pipe_spawn_time > PIPE_SPAWN_RATE:
                game.generate_pipe_pair()

            for pipe in game.pipes:
                if not pipe.passed and pipe.rect.right < game.bird.rect.left:
                    game.score += 1
                    pipe.passed = True

        game.pipes.draw(game.screen)
        game.screen.blit(game.bird.image, game.bird.rect)

        score_surf = game.font.render(f'Score: {game.score}', True, (0, 0, 0))
        game.screen.blit(score_surf, (10, 10))

        if game.game_over:
            game.show_game_over()

        pygame.display.flip()
        game.clock.tick(60)

    pygame.quit()
    sys.exit()
