import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1
FLY_SPEED = -15
OBSTACLE_WIDTH = 30
OBSTACLE_GAP_SIZE = 200
OBSTACLE_SPEED = 5
SCORE_FONT = pygame.font.Font(None, 36)


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

        self.spawn_obstacle()

    def spawn_obstacle(self):
        top = random.randint(0, HEIGHT - CAVERN_WIDTH)
        bottom = top + CAVERN_WIDTH
        obstacle_top = Obstacle(bottom=bottom)
        obstacle_bottom = Obstacle(top=top)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            self.all_sprites.update()

            hits = pygame.sprite.spritecollide(self.player, self.obstacles, False) or not 0 < self.player.rect.y < HEIGHT
            if hits:
                self.game_over = True

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.score += 1
            score_text = SCORE_FONT.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if not self.obstacles:
                self.spawn_obstacle()
            pygame.display.flip()
        else:
            game_over_text = SCORE_FONT.render('Game Over!', True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        self.clock.tick(FPS)
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if not 0 < self.rect.y < HEIGHT:
            self.kill()

    def jump(self):
        self.velocity = FLY_SPEED


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(right=WIDTH)

        if top is not None:
            self.rect.bottom = top
        elif bottom is not None:
            self.rect.top = bottom

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
        running = game.run(event)

    pygame.quit()