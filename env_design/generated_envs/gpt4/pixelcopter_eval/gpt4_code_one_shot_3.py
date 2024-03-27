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
        top = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        bottom = top + CAVERN_WIDTH
        new_obstacle = Obstacle(top, bottom)
        self.obstacles.add(new_obstacle)
        self.all_sprites.add(new_obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.score = 0
        self.spawn_obstacle()

    def update_score(self):
        self.score += 1
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(text, (10, 10))

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            # Update sprites and spawn new obstacles
            self.all_sprites.update()
            pygame.sprite.groupcollide(self.player, self.obstacles, False, True)

            if pygame.sprite.spritecollideany(self.player, self.obstacles):
                self.game_over = True
                font = pygame.font.SysFont(None, 74)
                text = font.render('Game Over!', True, WHITE)
                text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                self.screen.blit(text, text_rect)

            # Draw everything
            self.screen.fill(BLACK)
            self.update_score()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            # Ensure game runs at the correct framerate
            self.clock.tick(FPS)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

        # Spawn a new obstacle if there is space
        if not self.obstacles or self.obstacles.sprites()[-1].rect.right < WIDTH:
            self.spawn_obstacle()

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
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 1  # Apply gravity
        self.rect.y += self.velocity

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.kill()

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = -10


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
        width = random.randint(20, 60)
        self.image = pygame.Surface((width, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH

        if top and bottom:
            gap = pygame.Surface((width, bottom - top))
            gap.fill(BLACK)
            self.image.blit(gap, (0, top))

        self.velocity = -3

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x += self.velocity
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
