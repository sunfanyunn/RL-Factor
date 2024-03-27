import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
OBSTACLE_WIDTH = 30  # Width of the obstacles
OBSTACLE_GAP = 200  # Gap in milliseconds between each pair of obstacles

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.player = Pixelcopter(self)
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, OBSTACLE_GAP)

    def spawn_obstacle(self):
        gap_start = random.randint(CAVERN_WIDTH, HEIGHT - CAVERN_WIDTH)
        top_obstacle = Obstacle(self, bottom=gap_start - CAVERN_WIDTH // 2)
        bottom_obstacle = Obstacle(self, top=gap_start + CAVERN_WIDTH // 2)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.player.kill()
        self.player = Pixelcopter(self)
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.score = 0
        pygame.time.set_timer(self.obstacle_timer, OBSTACLE_GAP)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if not self.game_over:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.player.jump()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.jump()

                if event.type == self.obstacle_timer:
                    self.spawn_obstacle()

            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()

            if not self.game_over:
                self.all_sprites.update()
                self.score += 1 / FPS
                if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                    self.game_over = True

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            score_surf = self.font.render(f'Score: {int(self.score)}', True, WHITE)
            self.screen.blit(score_surf, (10, 10))

            if self.game_over:
                game_over_surf = self.font.render('Game Over! Press R to Restart', True, WHITE)
                game_over_rect = game_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(game_over_surf, game_over_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        if not self.game.game_over:
            self.velocity += 0.5  # Gravity
            self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        if not self.game.game_over:
            self.velocity = -10

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, top=None, bottom=None):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT // 2 - CAVERN_WIDTH // 2))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(midbottom=(WIDTH, top))
        elif bottom is not None:
            self.rect = self.image.get_rect(midtop=(WIDTH, bottom))

    def update(self):
        if not self.game.game_over:
            self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        game.run()
    pygame.quit()

