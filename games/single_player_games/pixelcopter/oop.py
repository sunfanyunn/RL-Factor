import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern


class PixelcopterGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.all_sprites.add(self.player)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        if random.randint(0, 100) < 20:  # Adjust the probability as needed
            gap_height = random.randint(50, 250)
            obstacle1 = Obstacle(HEIGHT - gap_height)
            obstacle2 = Obstacle(0, HEIGHT - gap_height - CAVERN_WIDTH)

            self.obstacles.add(obstacle1, obstacle2)
            self.all_sprites.add(obstacle1, obstacle2)
        else:
            obstacle = Obstacle()
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.player.jump()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.all_sprites.empty()
        self.obstacles.empty()

        self.player = Pixelcopter()
        self.all_sprites.add(self.player)

        self.spawn_obstacle()

    def update_game(self):
        if not self.game_over:
            self.all_sprites.update()
            self.spawn_obstacle()

            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True

            if self.player.rect.y > HEIGHT or self.player.rect.y < 0:
                self.game_over = True

    def render_game(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        if self.game_over:
            self.show_message("Game Over. Press R to restart.")

        pygame.display.flip()
        self.clock.tick(FPS)

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self):
        while True:
            self.handle_events()
            self.update_game()
            self.render_game()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += 0.5
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -8


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        if top is not None and bottom is not None:
            self.image = pygame.Surface((30, CAVERN_WIDTH))
            self.rect = self.image.get_rect(topleft=(WIDTH, top))
        else:
            self.image = pygame.Surface((30, random.randint(50, 200)))
            self.rect = self.image.get_rect(
                topleft=(WIDTH, HEIGHT - self.image.get_height())
            )

        self.image.fill(WHITE)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    game = PixelcopterGame()
    game.run()
