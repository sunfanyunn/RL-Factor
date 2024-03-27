import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
OBSTACLE_SPEED = 2
OBSTACLE_FREQUENCY = 2000  # Milliseconds


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
        self.obstacle_timer = pygame.time.get_ticks()
        self.spawn_obstacle()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top_height = random.randint(50, HEIGHT // 2 - CAVERN_WIDTH // 2)
        bottom_height = HEIGHT - (top_height + CAVERN_WIDTH)

        top_obstacle = Obstacle(top=top_height)
        bottom_obstacle = Obstacle(bottom=bottom_height)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

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
        self.obstacle_timer = pygame.time.get_ticks()
        self.spawn_obstacle()

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        if event.type == pygame.QUIT:
            return False
        if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.reset_game()

        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                self.player.jump()

            current_time = pygame.time.get_ticks()
            if current_time - self.obstacle_timer > OBSTACLE_FREQUENCY:
                self.obstacle_timer = current_time
                self.spawn_obstacle()

            self.all_sprites.update()

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT:
                self.game_over = True

            self.score += 1 / FPS
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.draw_score()
        else:
            self.draw_game_over()

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def draw_score(self):
        font = pygame.font.SysFont('arial', 32)
        text_surface = font.render('Score: ' + str(int(self.score)), True, WHITE)
        self.screen.blit(text_surface, (10, 10))

    def draw_game_over(self):
        font = pygame.font.SysFont('arial', 48)
        text_surface = font.render('GAME OVER!', True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.screen.blit(text_surface, text_rect)

        font = pygame.font.SysFont('arial', 22)
        text_surface = font.render('Press SPACE to restart', True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
        self.screen.blit(text_surface, text_rect)

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
        self.rect = self.image.get_rect(center=(WIDTH / 4, HEIGHT / 2))
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 0.5  # Gravity effect
        self.rect.y += int(self.velocity)

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
        if self.velocity > 0:  # Adds responsiveness to the controls
            self.velocity = 0
        self.velocity -= 10

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
        width = 20
        height = HEIGHT
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(topright=(WIDTH, 0))
            self.image = pygame.Surface((width, top))
        elif bottom is not None:
            self.rect = self.image.get_rect(bottomleft=(WIDTH, HEIGHT))
            self.image = pygame.Surface((width, bottom))
        self.image.fill(WHITE)

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()

