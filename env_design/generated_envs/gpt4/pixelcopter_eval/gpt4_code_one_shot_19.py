import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1
THRUST = -15
OBSTACLE_WIDTH = 50
OBSTACLE_GAP_SIZE = 200
OBSTACLE_FREQUENCY = 1500 # milliseconds


pygame.init()


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
        self.font = pygame.font.SysFont(None, 36)
        self.last_obstacle = pygame.time.get_ticks()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top = random.randint(0, HEIGHT - OBSTACLE_GAP_SIZE)
        bottom = top + OBSTACLE_GAP_SIZE
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
        self.score = 0
        self.last_obstacle = pygame.time.get_ticks()
        self.game_over = False

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            now = pygame.time.get_ticks()
            if now - self.last_obstacle > OBSTACLE_FREQUENCY:
                self.spawn_obstacle()
                self.last_obstacle = now

            self.all_sprites.update()
            self.player.update()
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            self.score += 1
            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()

            self.game_over = any(pygame.sprite.spritecollide(self.player, self.obstacles, False)) or self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT
            if self.game_over:
                game_over_text = self.font.render('Game Over!', True, WHITE)
                self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                self.reset_game()
        else:
            self.reset_game()
            self.game_over = False
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
        self.image = pygame.Surface((60, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.jump()

        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
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
            self.image.set_colorkey(BLACK)
            pygame.draw.rect(self.image, BLACK, [0, 0, OBSTACLE_WIDTH, top])
        if bottom is not None:
            self.image.set_colorkey(BLACK)
            pygame.draw.rect(self.image, BLACK, [0, bottom, OBSTACLE_WIDTH, HEIGHT - bottom])

        self.rect = self.image.get_rect(right=WIDTH)

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
