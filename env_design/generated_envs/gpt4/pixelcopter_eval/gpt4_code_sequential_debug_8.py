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
        self.score = 0

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_obstacle()

    def spawn_obstacle(self):
        gap_top = random.randint(0, HEIGHT - CAVERN_WIDTH)
        gap_bottom = gap_top + CAVERN_WIDTH

        top_obstacle = Obstacle(bottom=gap_top)
        bottom_obstacle = Obstacle(top=gap_bottom)

        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.player.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.player.velocity = 0

        for obstacle in self.obstacles:
            obstacle.kill()
        self.obstacles.empty()
        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            self.player.update()
            self.obstacles.update()
            self.score += 1
            is_collision = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if is_collision or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                self.game_over = True
            else:
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP)) or (event.type == pygame.MOUSEBUTTONDOWN):
                    self.player.jump()

                self.obstacles.update()

                # Spawn a new obstacle if the farthest one is past a certain point
                if not self.obstacles or self.obstacles.sprites()[-1].rect.right < WIDTH / 2:
                    self.spawn_obstacle()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect)

        score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = pygame.font.SysFont(None, 72).render('Game Over!', True, WHITE)
            restart_text = pygame.font.SysFont(None, 36).render('Press R to restart', True, WHITE)
            self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT // 2 - game_over_text.get_height() // 2)))
            self.screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, (HEIGHT // 2 + restart_text.get_height() // 2 + 20)))

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super(Pixelcopter, self).__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += 0.5  # Simulate gravity
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -10

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super(Obstacle, self).__init__()
        self.image = pygame.Surface((20, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(right=WIDTH)

        if top is not None:
            self.rect.y = 0
            self.rect.height = top
            self.image = self.image.subsurface(pygame.Rect(0, 0, 20, top))
        if bottom is not None:
            self.rect.y = bottom
            self.image = self.image.subsurface(pygame.Rect(0, 0, 20, HEIGHT - bottom))

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

