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
OBSTACLE_SPEED = 2
OBSTACLE_INTERVAL = 2000  # Milliseconds


class Game:
    def __init__(self):
        # Initialize the game components here
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
        self.spawn_obstacle()

    def spawn_obstacle(self):
        obstacle_top_height = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        obstacle_top = Obstacle(0, obstacle_top_height)
        obstacle_bottom = Obstacle(obstacle_top_height + CAVERN_WIDTH, HEIGHT)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.game_over = False
        self.score = 0

        for sprite in self.all_sprites:
            sprite.kill()

        self.player = Pixelcopter()
        self.all_sprites.add(self.player)

        self.obstacle_timer = pygame.time.get_ticks()

    def run(self, event):
        self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_SPACE and not self.game_over:
                    self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True

            current_time = pygame.time.get_ticks()
            if current_time - self.obstacle_timer > OBSTACLE_INTERVAL:
                self.spawn_obstacle()
                self.obstacle_timer = current_time
                self.score += 1

            self.screen.fill(BLACK)
            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.all_sprites.draw(self.screen)
        else:
            game_over_text = self.font.render('Game Over! Press R to restart', True, WHITE)
            self.screen.fill(BLACK)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(game_over_text, game_over_rect)

        pygame.display.flip()
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

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = FLAP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        super().__init__()
        self.image = pygame.Surface((30, bottom - top))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topright=(WIDTH, top))

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run(None)
    pygame.quit()
