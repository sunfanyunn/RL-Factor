import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_SPACING = 300
PIPE_SPEED = 5
BIRD_SIZE = 50
GRAVITY = 0.5
BIRD_JUMP = -10
BIRD_X = SCREEN_WIDTH // 4


class Bird(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_SIZE, BIRD_SIZE))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(BIRD_X, y))
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
        self.velocity = BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, orientation, height):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        if orientation == 'top':
            self.rect.bottomleft = (x, 0)
        else:
            self.rect.topleft = (x, SCREEN_HEIGHT)
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
        self.font = pygame.font.SysFont('Arial', 50)
        self.reset_game()

    def reset_game(self):
        self.bird_group = pygame.sprite.GroupSingle()
        self.pipe_group = pygame.sprite.Group()
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_HEIGHT // 2)
        self.bird_group.add(self.bird)
        self.generate_initial_pipes()
    
    def generate_initial_pipes(self):
        gap_y = random.randint(100, SCREEN_HEIGHT - 200)
        top_height = gap_y
        bottom_height = SCREEN_HEIGHT - gap_y - PIPE_SPACING
        self.pipes = [Pipe(SCREEN_WIDTH * 1.5, 'top', top_height), Pipe(SCREEN_WIDTH * 1.5, 'bottom', bottom_height)]
        for pipe in self.pipes:
            self.pipe_group.add(pipe)
    
    def run(self, event):
        if self.game_over:
            return False
        
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            self.bird.jump()

        self.screen.fill((0, 0, 0))
        self.bird_group.update()
        self.bird_group.draw(self.screen)

        self.pipe_group.update()
        self.pipe_group.draw(self.screen)

        if pygame.sprite.spritecollide(self.bird, self.pipe_group, False) or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.game_over = True

        self.handle_passed_pipes()

        score_text = self.font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, (255, 255, 255))
            self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))

        pygame.display.flip()
        self.clock.tick(30)

        # Automatically generate new pipes to maintain game difficulty
        last_pipe = self.pipe_group.sprites()[-1]
        if last_pipe.rect.right < SCREEN_WIDTH - PIPE_SPACING:
            self.generate_new_pipes()

        return True

    def handle_passed_pipes(self):
        for pipe in self.pipe_group.sprites():
            if not pipe.passed and pipe.rect.right < BIRD_X:
                pipe.passed = True
                self.score += 1

    def generate_new_pipes(self):
        gap_y = random.randint(100, SCREEN_HEIGHT - 200)
        top_height = gap_y
        bottom_height = SCREEN_HEIGHT - gap_y - PIPE_SPACING
        new_pipes = [Pipe(SCREEN_WIDTH, 'top', top_height), Pipe(SCREEN_WIDTH, 'bottom', bottom_height)]
        self.pipe_group.add(new_pipes[0], new_pipes[1])


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()


