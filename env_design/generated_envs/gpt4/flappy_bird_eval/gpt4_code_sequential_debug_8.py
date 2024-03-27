import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP_SIZE = 200
PIPE_SPEED = 5
BIRD_SIZE = 50
GRAVITY = 1
JUMP_HEIGHT = 12


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
        self.image.fill((255, 255, 0))  # Yellow color
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self, up_pressed):
        if up_pressed:
            self.jump()
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.y > SCREEN_HEIGHT - BIRD_SIZE:
            self.rect.y = SCREEN_HEIGHT - BIRD_SIZE
            self.velocity = 0
        self.rect.y = max(self.rect.y, 0)

    def jump(self):
        self.velocity = -JUMP_HEIGHT


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, centered_y, orientation):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT // 2 - PIPE_GAP_SIZE // 2))
        self.image.fill((0, 128, 0))  # Green color
        if orientation == 'bottom':
            self.rect = self.image.get_rect(midtop=(x, centered_y + PIPE_GAP_SIZE // 2))
        else:
            self.rect = self.image.get_rect(midbottom=(x, centered_y - PIPE_GAP_SIZE // 2))
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 64)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.all_sprites.add(self.bird)
        pygame.time.set_timer(pygame.USEREVENT, 2000)

    def spawn_pipes(self):
        center_gap_y = random.randint(PIPE_GAP_SIZE // 2 + PIPE_WIDTH, SCREEN_HEIGHT - (PIPE_GAP_SIZE // 2 + PIPE_WIDTH))
        top_pipe = Pipe(SCREEN_WIDTH, center_gap_y, 'top')
        bottom_pipe = Pipe(SCREEN_WIDTH, center_gap_y, 'bottom')
        self.all_sprites.add(top_pipe, bottom_pipe)
        self.pipes.add(top_pipe, bottom_pipe)

    def run(self, event):
        up_pressed = event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.game_over = True
        if self.game_over:
            self.show_game_over()
            self.clock.tick(60)
            return False
        elif event.type == pygame.USEREVENT:
            self.spawn_pipes()

        self.bird.update(up_pressed)
        self.pipes.update()
        self.check_collisions()

        self.screen.fill((135, 206, 250))  # Fill the screen with a skyblue color
        self.all_sprites.draw(self.screen)
        self.show_score()

        pygame.display.flip()
        self.clock.tick(60)

        return True

    def check_collisions(self):
        if pygame.sprite.spritecollideany(self.bird, self.pipes):
            self.game_over = True
        for pipe in self.pipes:
            if not pipe.passed and self.bird.rect.left > pipe.rect.right:
                pipe.passed = True
                self.score += 1

    def show_score(self):
        score_surface = self.font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(topleft=(20, 20))
        self.screen.blit(score_surface, score_rect)

    def show_game_over(self):
        game_over_surface = self.font.render('Game Over!', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            running = game.run(event)
    pygame.quit()

