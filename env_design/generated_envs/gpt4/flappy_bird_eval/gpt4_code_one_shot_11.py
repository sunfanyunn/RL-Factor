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
PIPE_SPAWN_RATE = 1500 # milliseconds


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, width=30, height=30):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.velocity = -BIRD_JUMP


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_upper=False, height=400):
        super().__init__()
        self.x = x
        self.height = height
        self.width = PIPE_WIDTH
        self.is_upper = is_upper
        y = 0 if is_upper else SCREEN_HEIGHT - height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_MOVE_SPEED


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.bird = Bird(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)
        self.pipes = pygame.sprite.Group()
        self.generate_pipe_pair()

    def run(self, event):
        self.screen.fill((135, 206, 250))  # Sky blue background

        # Event handling
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and not self.game_over:
            if event.key == pygame.K_UP:
                self.bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            self.bird.jump()

        # Game logic
        if not self.game_over:
            self.bird.update()
            self.pipes.update()
            for pipe in self.pipes:
                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)

            self.check_collisions()

            # Pipes generation
            now = pygame.time.get_ticks()
            if now - self.last_pipe_spawn_time > PIPE_SPAWN_RATE:
                self.generate_pipe_pair()

        # Draw everything
        pygame.draw.rect(self.screen, (255, 255, 255), self.bird.rect)
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (0, 128, 0), pipe.rect)

        # Score display
        score_surf = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))

        if self.game_over:
            self.show_game_over()

        pygame.display.flip()
        self.clock.tick(60)
        return True

    def check_collisions(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe):
                self.game_over = True
            if not pipe.passed and pipe.rect.centerx < self.bird.rect.left:
                self.score += 0.5  # Since there are two pipes for each point
                pipe.passed = True

    def generate_pipe_pair(self):
        pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP_SIZE - 50)
        self.pipes.add(Pipe(SCREEN_WIDTH, True, pipe_height))
        self.pipes.add(Pipe(SCREEN_WIDTH, False, SCREEN_HEIGHT - pipe_height - PIPE_GAP_SIZE))
        self.last_pipe_spawn_time = pygame.time.get_ticks()

    def show_game_over(self):
        game_over_surf = self.font.render('Game Over!', True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(game_over_surf, game_over_rect)


if __name__ == "__main__":
    game = Game()
    pygame.init()
    pygame.time.set_timer(pygame.USEREVENT+1, PIPE_SPAWN_RATE)
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
