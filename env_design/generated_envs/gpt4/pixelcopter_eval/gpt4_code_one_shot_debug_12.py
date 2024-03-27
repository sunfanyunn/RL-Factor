import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 0.5
FLYING_STRENGTH = -10
OBSTACLE_SPEED = 3


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        top = random.randint(0, HEIGHT - CAVERN_WIDTH)
        bottom = top + CAVERN_WIDTH

        obstacle_top = Obstacle(0, top)
        obstacle_bottom = Obstacle(bottom, HEIGHT)

        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.player.kill()
        self.obstacles.empty()
        self.all_sprites.empty()

        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.score = 0
        self.game_over = False

        self.spawn_obstacle()

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self.game_over:
                    self.reset_game()
                else:
                    self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            self.score += 1

            collision = pygame.sprite.spritecollideany(self.player, self.obstacles)
            if collision or not self.screen.get_rect().contains(self.player.rect):
                self.game_over = True
        else:
            last_obstacle = max(self.obstacles, key=lambda x: x.rect.right, default=None)
            if last_obstacle and last_obstacle.rect.right < WIDTH / 2:
                self.spawn_obstacle()

        for obstacle in list(self.obstacles):
            if obstacle.rect.right < 0:
                obstacle.kill()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score // FPS}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            restart_text = self.font.render('Click to restart', True, WHITE)
            self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 50))
            self.screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, HEIGHT // 2))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = FLYING_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, bottom, height):
        super().__init__()
        self.image = pygame.Surface((40, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.right = WIDTH
        if bottom is None:
            self.rect.top = 0
        else:
            self.rect.bottom = bottom

    def update(self):
        self.rect.x -= OBSTACLE_SPEED


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
