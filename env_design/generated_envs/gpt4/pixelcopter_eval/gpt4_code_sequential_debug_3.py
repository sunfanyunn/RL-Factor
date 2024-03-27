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
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.spawn_obstacle()
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.obstacle_timer = pygame.time.get_ticks()

    def spawn_obstacle(self):
        top_obstacle = Obstacle(top=True)
        bottom_obstacle = Obstacle(bottom=True)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_obstacle()
        self.score = 0
        self.obstacle_timer = pygame.time.get_ticks()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                self.player.jump()

            now = pygame.time.get_ticks()
            if now - self.obstacle_timer > 1500:
                self.spawn_obstacle()
                self.obstacle_timer = now

            self.all_sprites.update()

            if pygame.sprite.spritecollideany(self.player, self.obstacles):
                self.game_over = True
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.reset_game()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        if self.game_over:
            text_surface = self.font.render('Game Over!', True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
            text_surface = self.font.render('Press Space to restart', True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(text_surface, text_rect)
        else:
            self.score += 1 / FPS
            score_surface = self.font.render(f'Score: {int(self.score)}', True, WHITE)
            self.screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.centery = HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += 0.5  # Simulate gravity
        self.rect.y += int(self.velocity)

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        self.velocity = -10  # Jump upwards


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        width = WIDTH
        gap_center = random.randint(100, HEIGHT - 100)
        gap_height = 150

        if top:
            self.image = pygame.Surface((CAVERN_WIDTH, gap_center - gap_height // 2))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect(topright=(WIDTH, 0))
        elif bottom:
            self.image = pygame.Surface((CAVERN_WIDTH, HEIGHT - (gap_center + gap_height // 2)))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect(bottomright=(WIDTH, HEIGHT))
        self.rect.x -= WIDTH

    def update(self):
        self.rect.x -= 2
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
