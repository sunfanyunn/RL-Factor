import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 0.6
JUMP_STRENGTH = -10
OBSTACLE_WIDTH = 30
OBSTACLE_SPEED = 3
OBSTACLE_GAP_SIZE = 200
OBSTACLE_FREQUENCY = 1500


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.obstacle_timer = pygame.time.get_ticks()

    def spawn_obstacle(self):
        middle_pos = random.randint(OBSTACLE_GAP_SIZE // 2, HEIGHT - OBSTACLE_GAP_SIZE // 2)
        bottom_obstacle = Obstacle(bottom=middle_pos + OBSTACLE_GAP_SIZE // 2)
        top_obstacle = Obstacle(top=middle_pos - OBSTACLE_GAP_SIZE // 2)
        self.all_sprites.add(bottom_obstacle, top_obstacle)
        self.obstacles.add(bottom_obstacle, top_obstacle)

    def reset_game(self):
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.obstacle_timer = pygame.time.get_ticks()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if self.game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            self.reset_game()

        self.screen.fill(BLACK)
        if not self.game_over:
            self.player.update()
            now = pygame.time.get_ticks()
            if now - self.obstacle_timer > OBSTACLE_FREQUENCY:
                self.spawn_obstacle()
                self.obstacle_timer = now

            self.obstacles.update()
            self.all_sprites.draw(self.screen)

            if self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT or pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True
        else:
            font = pygame.font.SysFont('Arial', 36)
            text_surface = font.render('Game Over!', True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
        self.clock.tick(FPS)

        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((CAVERN_WIDTH, CAVERN_WIDTH))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(right=WIDTH)
        if top is not None:
            self.rect.top = 0
            self.rect.height = top
        elif bottom is not None:
            self.rect.bottom = HEIGHT
            self.rect.height = HEIGHT - bottom

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
        if event.type == pygame.NOEVENT:
            continue
        running = game.run(event)
    pygame.quit()
