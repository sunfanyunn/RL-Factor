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
        self.score = 0

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        if not self.obstacles or self.obstacles.sprites()[-1].rect.right < WIDTH - 300:
            top = random.randint(0, HEIGHT // 2 - CAVERN_WIDTH)
            bottom = top + CAVERN_WIDTH
            obstacle = Obstacle(top=top, bottom=bottom)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.obstacles.empty()
        self.all_sprites.empty()
        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.spawn_obstacle()
        self.score = 0

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        self.clock.tick(FPS)
        self.screen.fill(BLACK)

        self.player.update()
        self.obstacles.update()

        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not self.game_over:
                self.player.jump()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()

        self.spawn_obstacle()

        if pygame.sprite.spritecollideany(self.player, self.obstacles) or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
            self.game_over = True
        else:
            self.score += 1

        self.all_sprites.draw(self.screen)

        score_text = pygame.font.SysFont(None, 30).render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = pygame.font.SysFont(None, 74).render('Game Over! Press R to Restart', True, WHITE)
            game_over_rect = game_over_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(game_over_text, game_over_rect)

        pygame.display.flip()
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the Pixelcopter
        self.image is the Pygame Surface representing the Pixelcopter
        self.rect is the Pygame Rect representing the Pixelcopter's position and size
        self.velocity is the Pixelcopter's vertical velocity
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 0.5  # Gravity
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = -10  # Jump velocity


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        """
        Initialize an obstacle
        top is the top y-coordinate of the obstacle's gap (if applicable)
        bottom is the bottom y-coordinate of the obstacle's gap (if applicable)
        self.image is the Pygame Surface representing the obstacle
        self.rect is the Pygame Rect representing the obstacle's position and size
        """
        super().__init__()
        self.image = pygame.Surface((20, HEIGHT))
        self.image.fill(WHITE)

        if top is not None and bottom is not None:
            top_part = pygame.Surface((20, top))
            top_part.fill(BLACK)
            bottom_part = pygame.Surface((20, HEIGHT - bottom))
            bottom_part.fill(BLACK)

            self.image.blit(top_part, (0, 0))
            self.image.blit(bottom_part, (0, bottom))
        self.rect = self.image.get_rect(midtop=(WIDTH, 0))

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= 2  # Move the obstacle left
        if self.rect.right < 0:
            self.kill()  # Remove the obstacle when it's no longer on the screen


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()
