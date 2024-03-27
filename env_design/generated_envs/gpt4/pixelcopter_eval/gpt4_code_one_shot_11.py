import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100


# Player character represented as a helicopter
class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        keys = pygame.key.get_pressed()
        mouse_down = pygame.mouse.get_pressed()[0]
        if keys[pygame.K_SPACE] or mouse_down:
            self.jump()

        # Apply gravity
        self.velocity += 1
        self.rect.y += self.velocity

        # Prevent the helicopter from moving off-screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, y_pos, height):
        super().__init__()
        self.image = pygame.Surface((20, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=(WIDTH, y_pos))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


class Game:
    def __init__(self):
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
        height = random.randint(100, HEIGHT - 100 - CAVERN_WIDTH)
        top_obstacle = Obstacle(0, height)
        bottom_obstacle = Obstacle(height + CAVERN_WIDTH, HEIGHT - height)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # Set the spawn obstacle event

    def reset_game(self):
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.game_over = False
        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()
        else:
            self.screen.fill(BLACK)
            self.all_sprites.update()

            # Check collisions
            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True

            # Update and draw all sprites
            self.all_sprites.draw(self.screen)

            # Scoring
            self.score += 1
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

            # Spawn obstacles
            if event.type == pygame.USEREVENT + 1:
                self.spawn_obstacle()

            pygame.display.flip()
            self.clock.tick(FPS)

        return True


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
