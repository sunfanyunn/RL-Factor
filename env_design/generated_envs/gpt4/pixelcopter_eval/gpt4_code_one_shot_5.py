import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1
FLAP_STRENGTH = -12
OBSTACLE_SPEED = 3
OBSTACLE_INTERVAL = 1800  # Milliseconds


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.obstacle_timer = pygame.time.get_ticks()

        self.all_sprites.add(self.player)

    def spawn_obstacle(self):
        obstacle_top = Obstacle(bottom=random.randint(CAVERN_WIDTH + 20, HEIGHT - 20))
        obstacle_bottom = Obstacle(top=obstacle_top.rect.bottom + CAVERN_WIDTH)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.obstacle_timer = pygame.time.get_ticks()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            current_time = pygame.time.get_ticks()
            if current_time - self.obstacle_timer > OBSTACLE_INTERVAL:
                self.spawn_obstacle()
                self.obstacle_timer = current_time

            self.all_sprites.update()
            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or not 0 <= self.player.rect.y <= HEIGHT:
                self.game_over = True
                game_over_text = self.font.render('Game Over!', True, WHITE)
                game_over_rect = game_over_text.get_rect()
                game_over_rect.center = (WIDTH // 2, HEIGHT // 2)
                self.screen.blit(game_over_text, game_over_rect)

            else:
                self.score += 1
                self.screen.fill(BLACK)
                score_text = self.font.render(f'Score: {self.score}', True, WHITE)
                self.screen.blit(score_text, (10, 10))
                self.obstacles.update()
                self.all_sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()

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
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = FLAP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((40, HEIGHT))
        self.image.fill(WHITE)

        if top is None and bottom is not None:
            self.rect = self.image.get_rect(topleft=(WIDTH, bottom - self.image.get_height()))
        elif bottom is None and top is not None:
            self.rect = self.image.get_rect(topleft=(WIDTH, top))

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
