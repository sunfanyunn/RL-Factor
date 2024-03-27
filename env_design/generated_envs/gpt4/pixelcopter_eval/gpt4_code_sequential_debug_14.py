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
        """
        Initialize the game
        self.screen is the Pygame display surface
        self.clock is the Pygame Clock
        self.game_over is a boolean representing whether the game is over
        self.player is the Pixelcopter instance
        self.obstacles is a Pygame sprite Group containing Obstacle instances
        self.all_sprites is a Pygame sprite Group containing all sprites
        """
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_obstacle()

        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        self.obstacle_timer = pygame.time.get_ticks()

    def spawn_obstacle(self):
        top = random.randint(0, HEIGHT - CAVERN_WIDTH)
        bottom = top + CAVERN_WIDTH
        obstacle_top = Obstacle(bottom=top)
        obstacle_bottom = Obstacle(top=bottom)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.game_over = False
        self.score = 0

        self.obstacles.empty()
        self.all_sprites.empty()

        self.player = Pixelcopter()
        self.all_sprites.add(self.player)

        self.spawn_obstacle()
        self.obstacle_timer = pygame.time.get_ticks()

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            return True

        if event and event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event and ((event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN)):
            self.player.jump()

        self.all_sprites.update()
        self.screen.fill(BLACK)

        current_time = pygame.time.get_ticks()
        if current_time - self.obstacle_timer > 2000:
            self.spawn_obstacle()
            self.obstacle_timer = current_time

        self.score += int(self.clock.get_time() / 1000)

        if (pygame.sprite.spritecollide(self.player, self.obstacles, False)
            or self.player.rect.top <= 0
            or self.player.rect.bottom >= HEIGHT):
            self.game_over = True
            self.display_game_over()

        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

        self.clock.tick(FPS)
        return True

    def display_game_over(self):
        text = self.font.render('Game Over! Press R to Restart', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        # If the game is over, the copter shouldn't move
        if game.game_over:
            return

        self.velocity += 0.5  # Gravity
        self.rect.y += int(self.velocity)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        width = WIDTH // 20
        height = HEIGHT - CAVERN_WIDTH
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)

        if top is not None:
            self.rect = self.image.get_rect(topleft=(WIDTH, top-height))
        elif bottom is not None:
            self.rect = self.image.get_rect(topright=(WIDTH, bottom))

    def update(self):
        # If the game is over, the obstacles shouldn't move
        if game.game_over:
            return

        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        else:
            game.run(event)
    pygame.quit()


