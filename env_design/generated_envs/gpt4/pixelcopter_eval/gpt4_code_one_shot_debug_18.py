import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 0.5
FLAP_STRENGTH = -10
OBSTACLE_SPEED = 5
OBSTACLE_INTERVAL = 2000  # Spawn a new obstacle every 2 seconds in milliseconds


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.scoring_system = pygame.font.SysFont('Comic Sans MS', 30)
        self.game_over = False

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.obstacle_timer = pygame.time.get_ticks()
        self.score = 0

    def spawn_obstacle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.obstacle_timer >= OBSTACLE_INTERVAL:
            self.obstacle_timer = current_time
            top_obstacle = Obstacle(bottom=random.randint(50, HEIGHT - CAVERN_WIDTH - 50))
            bottom_obstacle = Obstacle(top=top_obstacle.rect.bottom + CAVERN_WIDTH)
            self.obstacles.add(top_obstacle, bottom_obstacle)
            self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.player.kill()
        for obstacle in self.obstacles:
            obstacle.kill()
        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.obstacle_timer = pygame.time.get_ticks()
        self.score = 0

    def run(self, event):
        if event and event.type == pygame.QUIT:
            return False

        if not self.game_over:
            self.spawn_obstacle()

            if event and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                self.player.jump()

            self.all_sprites.update()
            self.screen.fill(BLACK)

            if pygame.sprite.spritecollideany(self.player, self.obstacles) or \
               not 0 <= self.player.rect.centery <= HEIGHT:
                self.game_over = True

            score_surface = self.scoring_system.render(f'Score: {int(self.score)}', False, WHITE)
            self.screen.blit(score_surface, (10, 10))

            self.score += 1 / FPS

        else:
            game_over_surface = self.scoring_system.render('Game Over! Click or Press any key to restart', False, WHITE)
            self.screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - game_over_surface.get_height() // 2))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def jump(self):
        self.velocity = FLAP_STRENGTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((40, HEIGHT//2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(x=WIDTH)
        if top is not None:
            self.rect.top = top - self.rect.height
        elif bottom is not None:
            self.rect.bottom = bottom

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
