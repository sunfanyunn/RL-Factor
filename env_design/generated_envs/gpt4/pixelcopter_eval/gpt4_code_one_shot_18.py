import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1
FLAP_STRENGTH = -10
OBSTACLE_SPEED = 5
OBSTACLE_INTERVAL = FPS * 2  # Spawn a new obstacle every 2 seconds


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

        self.score = 0
        self.scoring_system = pygame.font.SysFont('Comic Sans MS', 30)

        self.obstacle_timer = pygame.time.get_ticks()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        if pygame.time.get_ticks() - self.obstacle_timer > OBSTACLE_INTERVAL:
            self.obstacle_timer = pygame.time.get_ticks()
            top_obstacle = Obstacle(bottom=random.randint(50, HEIGHT - CAVERN_WIDTH - 50))
            bottom_obstacle = Obstacle(top=top_obstacle.rect.bottom + CAVERN_WIDTH)
            self.obstacles.add(top_obstacle, bottom_obstacle)
            self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.obstacles.empty()
        self.all_sprites.empty()
        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.score = 0
        self.obstacle_timer = pygame.time.get_ticks()

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if not self.game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            self.spawn_obstacle()
            self.score += 1
        else:
            self.reset_game()

        # Collision detection
        if pygame.sprite.spritecollideany(self.player, self.obstacles) or not 0 <= self.player.rect.y <= HEIGHT:
            self.game_over = True

        # Drawing everything
        self.screen.fill(BLACK)
        if self.game_over:
            game_over_text = self.scoring_system.render('Game Over!', False, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        else:
            self.all_sprites.draw(self.screen)
            # Draw score
            score_surface = self.scoring_system.render(f'Score: {self.score}', False, WHITE)
            self.screen.blit(score_surface, (10, 10))
        pygame.display.flip()
        self.clock.tick(FPS)

        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the Pixelcopter
        self.image is the Pygame Surface representing the Pixelcopter
        self.rect is the Pygame Rect representing the Pixelcopter's position and size
        self.velocity is the Pixelcopter's vertical velocity
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.centery = HEIGHT // 2
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = FLAP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        """
        Initialize an obstacle
        top is the top y-coordinate of the obstacle's gap (if applicable)
        bottom is the bottom y-coordinate of the obstacle's gap (if applicable)
        self.image is the Pygame Surface representing the obstacle
        self.rect is the Pygame Rect representing the obstacle's position and size
        """
        pygame.sprite.Sprite.__init__(self)
        if top is None and bottom is not None:
            self.image = pygame.Surface((40, bottom))
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.rect.bottom = bottom
        elif bottom is None and top is not None:
            self.image = pygame.Surface((40, HEIGHT - top))
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            self.rect.top = top
        self.image.fill(WHITE)

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:  # If the obstacle is no longer visible, remove it
            self.kill()


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
