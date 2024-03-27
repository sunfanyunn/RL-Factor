import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GRAVITY = 1
FLAP_STRENGTH = -10
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 400
OBSTACLE_GAP_SIZE = 150
OBSTACLE_SPEED = 2


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

        self.spawn_obstacle()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top_gap = random.randrange(50, HEIGHT - OBSTACLE_GAP_SIZE - 50)
        bottom_gap = top_gap + OBSTACLE_GAP_SIZE

        top_obstacle = Obstacle(bottom=top_gap)
        bottom_obstacle = Obstacle(top=bottom_gap)

        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(self.obstacles)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.player.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.player.velocity = 0
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_obstacle()
        self.score = 0

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and not self.game_over:
            if event.key == pygame.K_SPACE:
                self.player.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            self.player.jump()

        if not self.game_over:
            self.all_sprites.update()

            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True

            for obstacle in self.obstacles:
                if obstacle.rect.right < 0:
                    obstacle.kill()
                    self.score += 1

            # Periodically spawn new obstacles
            if len(self.obstacles) < 6:
                self.spawn_obstacle()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # Display the score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            text_rect = game_over_text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            self.screen.blit(game_over_text, text_rect)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(FPS)

        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Prevent the player from moving off-screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = FLAP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH

        if top is not None:
            self.rect.top = top - OBSTACLE_HEIGHT
        elif bottom is not None:
            self.rect.bottom = bottom

    def update(self):
        self.rect.x -= OBSTACLE_SPEED


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
