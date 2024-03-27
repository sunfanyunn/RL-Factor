
import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PLAYER_SIZE = 50
GRAVITY = 0.5
THRUST = -10
CAVERN_WIDTH = 100  # Width of the gap in the cavern
OBSTACLE_WIDTH = 70
OBSTACLE_SPEED = 3
SPAWN_INTERVAL = 1500


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
        self.score is the score of the game
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.spawn_timer = pygame.time.get_ticks()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top = random.randint(0, HEIGHT // 2)
        bottom = top + CAVERN_WIDTH

        obstacle_top = Obstacle(bottom=bottom)
        obstacle_bottom = Obstacle(top=top)

        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.game_over = False
        self.score = 0
        self.spawn_timer = pygame.time.get_ticks()

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
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_timer > SPAWN_INTERVAL:
                self.spawn_timer = current_time
                self.spawn_obstacle()

            self.all_sprites.update()
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.score += 1
            score_text = self.font.render(str(self.score), True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True
                game_over_text = self.font.render('Game Over!', True, WHITE)
                self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2,
                                                  HEIGHT // 2 - game_over_text.get_height() // 2))

        elif self.game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            self.reset_game()

        pygame.display.update()
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
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = THRUST


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
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        self.image.fill(WHITE)

        if top is not None:
            self.rect = self.image.get_rect(midbottom=(WIDTH, top))
        elif bottom is not None:
            self.rect = self.image.get_rect(midtop=(WIDTH, bottom))

    def update(self):
        """
        Update the obstacle's position
        """
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

