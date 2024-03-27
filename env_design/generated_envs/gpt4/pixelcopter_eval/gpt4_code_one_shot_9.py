
import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
OBSTACLE_WIDTH = 50  # Width of the obstacles
OBSTACLE_GAP_SIZE = 200  # Vertical gap size between the top and bottom obstacles
OBSTACLE_SPEED = 2  # Horizontal speed of the obstacles
PLAYER_SIZE = 32  # Size of the Pixelcopter
PLAYER_GRAVITY = 0.5  # Downward acceleration
PLAYER_JUMP_STRENGTH = -10  # Upward velocity when jumping


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
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.score = 0
        self.font = pygame.font.Font(None, 36)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top_gap = random.randint(50, HEIGHT - OBSTACLE_GAP_SIZE - 50)
        bottom_gap = top_gap + OBSTACLE_GAP_SIZE

        top_obstacle = Obstacle(bottom=bottom_gap)
        bottom_obstacle = Obstacle(top=top_gap)

        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.all_sprites.empty()
        self.obstacles.empty()
        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.game_over = False
        self.score = 0

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        self.clock.tick(FPS)
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_over:
                self.reset_game()
            else:
                self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            for obstacle in self.obstacles:
                if obstacle.rect.right < 0:
                    self.obstacles.remove(obstacle)
                    self.all_sprites.remove(obstacle)
                    self.score += 1
                    self.spawn_obstacle()

            if pygame.sprite.spritecollideany(self.player, self.obstacles):
                self.game_over = True

            if self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT:
                self.game_over = True

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(text, (10, 10))

            if self.game_over:
                game_over_text = self.font.render('Game Over!', True, WHITE)
                text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
                self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += PLAYER_GRAVITY
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = PLAYER_JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(topleft=(WIDTH, 0))
            self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, top))
        elif bottom is not None:
            self.rect = self.image.get_rect(bottomleft=(WIDTH, HEIGHT))
            self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, HEIGHT - bottom))

    def update(self):
        self.rect.x -= OBSTACLE_SPEED


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

