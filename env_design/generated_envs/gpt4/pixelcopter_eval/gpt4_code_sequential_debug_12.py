import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_SPEED = -5
HELICOPTER_SIZE = 32


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)
        self.spawn_obstacle()
        self.all_sprites.add(self.player)

    def spawn_obstacle(self):
        # The space where the Pixelcopter can pass through
        pass_through_offset = random.randint(0, HEIGHT - CAVERN_WIDTH - 10) + 5
        obstacle_top = Obstacle(top=pass_through_offset)
        obstacle_bottom = Obstacle(bottom=pass_through_offset + CAVERN_WIDTH)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.obstacles.empty()
        self.all_sprites.empty()

        self.game_over = False
        self.score = 0
        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.spawn_obstacle()

    def run(self, event):
        self.screen.fill(BLACK)
        if not self.game_over:
            self.all_sprites.update()

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if hits or self.player.rect.bottom > HEIGHT or self.player.rect.top < 0:
                self.game_over = True

            # Spawn a new obstacle if needed
            if self.obstacles.sprites() and self.obstacles.sprites()[-1].rect.right < WIDTH - 200:
                self.spawn_obstacle()

            # Remove off-screen obstacles
            for obstacle in self.obstacles:
                if obstacle.rect.right < 0:
                    obstacle.kill()

            self.all_sprites.draw(self.screen)
            # Increase score based on helicopter movement and draw it
            self.score += 1
            score_text = self.font.render(str(self.score), True, WHITE)
            self.screen.blit(score_text, (10, 10))

        else:
            game_over_text = self.font.render('Game Over! Press R to Restart', True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
        pygame.display.flip()
        self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.run(event)
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((HELICOPTER_SIZE, HELICOPTER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        width = WIDTH // 10
        if top is not None:
            height = top
            y = 0
        elif bottom is not None:
            height = HEIGHT - bottom
            y = bottom
        else:
            raise ValueError('Either top or bottom must be specified')

        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topright=(WIDTH, y))

    def update(self):
        self.rect.x += OBSTACLE_SPEED


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.handle_events()
    pygame.quit()

