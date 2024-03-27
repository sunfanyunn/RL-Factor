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

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        self.distance = 0  # Tracks the distance traveled

        for _ in range(5):
            self.spawn_obstacle()

    def spawn_obstacle(self):
        last_obstacle = max(self.obstacles, key=lambda o: o.rect.right, default=None)
        cavern_gap = random.randint(50, HEIGHT - CAVERN_WIDTH - 50)
        obstacle = Obstacle(top=cavern_gap, bottom=cavern_gap + CAVERN_WIDTH)
        obstacle.rect.left = WIDTH if last_obstacle is None else last_obstacle.rect.right + 250
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.distance = 0
        self.player.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.player.velocity = 0
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        for _ in range(5):
            self.spawn_obstacle()

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()
            return True

        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.jump()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.player.jump()

        self.all_sprites.update()

        if len(self.obstacles) < 6:
            self.spawn_obstacle()

        # Increment the distance and score based on distance traveled
        self.distance += 2
        self.score = self.distance // 100

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
            self.show_game_over_screen()
        else:
            pygame.display.flip()
            self.clock.tick(FPS)

        return True

    def show_game_over_screen(self):
        self.game_over = True
        game_over_text = self.font.render('Game Over! Press Space to Retry', True, WHITE)
        self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
        pygame.display.flip()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        if not game.game_over:
            self.velocity += 0.5  # Gravity effect
            self.rect.y += int(self.velocity)
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    def jump(self):
        self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((20, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        if top is not None and bottom is not None:
            pygame.draw.rect(self.image, BLACK, pygame.Rect(0, top, 20, bottom - top))

    def update(self):
        if not game.game_over:
            self.rect.x -= 2
            if self.rect.right < 0:
                self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

