import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.font = pygame.font.SysFont("Arial", 32)

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.obstacle_timer = 0
        self.spawn_obstacle()

        self.score = 0

    def spawn_obstacle(self):
        top = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        obstacle_top = Obstacle(bottom=top)
        obstacle_bottom = Obstacle(top=top + CAVERN_WIDTH)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.player.kill()
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.score = 0
        self.obstacle_timer = 0
        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        self.handle_input()

        if not self.game_over:
            self.all_sprites.update()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            self.score += 1
            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True

            self.obstacle_timer += 1
            if self.obstacle_timer >= 90:
                self.obstacle_timer = 0
                self.spawn_obstacle()

            pygame.display.flip()
        else:
            self.show_game_over()
            pygame.display.flip()

        self.clock.tick(FPS)
        return not self.game_over

    def show_game_over(self):
        game_over_font = pygame.font.SysFont("Arial", 72)
        game_over_text = game_over_font.render('Game Over!', True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        restart_font = pygame.font.SysFont("Arial", 32)
        restart_text = restart_font.render('Press R to Restart', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and self.game_over:
            self.reset_game()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.velocity = -10
        else:
            self.velocity += 0.5

        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((30, HEIGHT))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(midbottom=(WIDTH, top))
        elif bottom is not None:
            self.rect = self.image.get_rect(midtop=(WIDTH, bottom))
            self.rect.height = HEIGHT - bottom

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    game = Game()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game.run(event):
            break
