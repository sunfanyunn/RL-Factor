import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

OBSTACLE_WIDTH = 50
OBSTACLE_GAP_SIZE = 200
OBSTACLE_SPEED = 2
PLAYER_SIZE = 32
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_STRENGTH = -10


class Game:
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

        self.score = 0
        self.font = pygame.font.Font(None, 36)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        top_gap = random.randint(50, HEIGHT - OBSTACLE_GAP_SIZE - 50)
        bottom_gap = top_gap + OBSTACLE_GAP_SIZE

        top_obstacle = Obstacle(bottom=top_gap)
        bottom_obstacle = Obstacle(top=bottom_gap)

        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.all_sprites.empty()
        self.obstacles.empty()
        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.game_over = False
        self.score = 0

    def run(self, event):
        self.clock.tick(FPS)
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_over:
                self.reset_game()
                self.spawn_obstacle()
            else:
                self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            self.obstacles.update()
            self.score += 1

            for obstacle in list(self.obstacles):
                if obstacle.rect.right < 0:
                    self.obstacles.remove(obstacle)
                    self.all_sprites.remove(obstacle)
                    self.spawn_obstacle()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            text = self.font.render(f'Score: {self.score // 100}', True, WHITE)
            self.screen.blit(text, (10, 10))

            if pygame.sprite.spritecollideany(self.player, self.obstacles):
                self.game_over = True

            if self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT:
                self.game_over = True

            if self.game_over:
                game_over_text = self.font.render('Game Over!', True, WHITE)
                text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += PLAYER_GRAVITY
        self.rect.y += int(self.velocity)

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = PLAYER_JUMP_STRENGTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        if top is not None:
            self.image = pygame.Surface((OBSTACLE_WIDTH, top))
            self.rect = self.image.get_rect(topleft=(WIDTH, 0))
        elif bottom is not None:
            self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT - bottom))
            self.rect = self.image.get_rect(bottomleft=(WIDTH, HEIGHT))

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)

    pygame.quit()
