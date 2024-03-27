import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_MOVEMENT_SPEED = -5
BIRD_JUMP_STRENGTH = -10
GRAVITY = 1


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def jump(self):
        self.velocity = BIRD_JUMP_STRENGTH


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        top_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.image = pygame.Surface((PIPE_WIDTH, top_height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.bottom_image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT - top_height - PIPE_GAP))
        self.bottom_image.fill((0, 255, 0))
        self.bottom_rect = self.bottom_image.get_rect(topleft=(x, top_height + PIPE_GAP))
        self.passed = False

    def update(self):
        self.rect.x += PIPE_MOVEMENT_SPEED
        self.bottom_rect.x += PIPE_MOVEMENT_SPEED
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 72)
        self.reset_game()
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer, 1500)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.bird)
        new_pipe = Pipe(SCREEN_WIDTH)
        self.pipes.add(new_pipe)
        self.all_sprites.add(new_pipe)

    def run(self, event):
        if not self.game_over:
            self.bird.update()
            self.pipes.update()

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key in {pygame.K_SPACE, pygame.K_UP}:
                self.bird.jump()

            if event.type == self.pipe_timer:
                new_pipe = Pipe(SCREEN_WIDTH)
                self.pipes.add(new_pipe)
                self.all_sprites.add(new_pipe)

            for pipe in self.pipes:
                if not pipe.passed and pipe.rect.right < self.bird.rect.left:
                    pipe.passed = True
                    self.score += 1

            self.check_collisions()

            self.screen.fill((135, 206, 235))
            
            for sprite in self.all_sprites:
                if isinstance(sprite, Pipe):
                    self.screen.blit(sprite.image, sprite.rect)
                    self.screen.blit(sprite.bottom_image, sprite.bottom_rect)
                else:
                    self.screen.blit(sprite.image, sprite.rect)

            if self.game_over:
                self.show_game_over()
            else:
                self.show_score()
            
            pygame.display.flip()
            self.clock.tick(30)
        return True

    def check_collisions(self):
        for pipe in self.pipes:
            if pipe.rect.colliderect(self.bird.rect) or pipe.bottom_rect.colliderect(self.bird.rect):
                self.game_over = True

    def show_score(self):
        score_text = self.font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def show_game_over(self):
        game_over_text = self.font.render('Game Over!', True, (255,255,255))
        self.screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, (SCREEN_HEIGHT - game_over_text.get_height()) // 2))

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()