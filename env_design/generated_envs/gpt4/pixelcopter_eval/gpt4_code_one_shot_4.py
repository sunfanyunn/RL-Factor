import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern

# Define constants for player
PLAYER_SIZE = 50
GRAVITY = 0.6
JUMP_STRENGTH = -10

# Obstacle settings
OBSTACLE_WIDTH = 30
OBSTACLE_SPEED = 3
OBSTACLE_GAP_SIZE = 200
OBSTACLE_FREQUENCY = 1500 # in milliseconds


class Game:
    def __init__(self):
        """
        Initialize the game
        """
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.obstacle_timer = pygame.time.get_ticks()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top = random.randint(10, HEIGHT - OBSTACLE_GAP_SIZE - 10)
        bottom = top + OBSTACLE_GAP_SIZE
        obstacle_top = Obstacle(bottom=bottom)
        obstacle_bottom = Obstacle(top=top)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.score = 0
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.obstacle_timer = pygame.time.get_ticks()

    def run(self, event):
        """
        Run the game loop
        """
        self.screen.fill(BLACK)

        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            now = pygame.time.get_ticks()
            if now - self.obstacle_timer > OBSTACLE_FREQUENCY:
                self.obstacle_timer = now
                self.spawn_obstacle()
            self.player.update()
            self.obstacles.update()
            self.score += 1

            for obstacle in self.obstacles:
                if self.player.rect.colliderect(obstacle.rect):
                    self.game_over = True

            if self.game_over:
                self.screen.fill(BLACK)
                font = pygame.font.SysFont("Arial", 36)
                text_surface = font.render("Game Over!", True, WHITE)
                text_rect = text_surface.get_rect()
                text_rect.center = (WIDTH // 2, HEIGHT // 2)
                self.screen.blit(text_surface, text_rect)
            else:
                self.all_sprites.draw(self.screen)

                font = pygame.font.SysFont("Arial", 28)
                score_surface = font.render(f"Score: {self.score}", True, WHITE)
                self.screen.blit(score_surface, (10, 10))

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.jump()
        else:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(FPS)
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the Pixelcopter
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
        self.rect.y = max(self.rect.y, 0)
        self.rect.y = min(self.rect.y, HEIGHT - PLAYER_SIZE)

    def jump(self):
        """
        Make the Pixelcopter jump
        """
        self.velocity = JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        """
        Initialize an obstacle
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        if top is not None:
            self.image.fill(BLACK)
            self.rect = self.image.get_rect(bottomleft=(WIDTH, top))
        elif bottom is not None:
            self.image.fill(BLACK)
            self.rect = self.image.get_rect(topleft=(WIDTH, bottom))

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
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
