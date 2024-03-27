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

        self.score = 0
        self.spawn_obstacle()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top_gap = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        bottom_gap = top_gap + CAVERN_WIDTH
        new_obstacle_top = Obstacle(bottom=top_gap)
        new_obstacle_bottom = Obstacle(top=bottom_gap)
        self.obstacles.add(new_obstacle_top, new_obstacle_bottom)
        self.all_sprites.add(new_obstacle_top, new_obstacle_bottom)

    def reset_game(self):
        """
        Reset the game to its initial state
        """
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.empty()
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

        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.jump()
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            if event.button == 1:
                self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            self.screen.fill(BLACK)

            if self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                self.game_over = True

            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True

            obstacle_list = self.obstacles.sprites()
            for obstacle in obstacle_list:
                if obstacle.rect.right < 0 and obstacle.can_spawn_next:
                    self.spawn_obstacle()
                if obstacle.rect.right < obstacle.rect.width and not obstacle.can_spawn_next:
                    self.score += 1
                    obstacle.can_spawn_next = False

            score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            self.all_sprites.draw(self.screen)

            pygame.display.flip()

        else:
            message = pygame.font.SysFont(None, 48).render('Game Over! Press R to reset', True, WHITE)
            message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(message, message_rect)
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
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 0.5  # simulate gravity
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
        self.image = pygame.Surface((30, HEIGHT))
        self.image.fill(WHITE)

        if top is None:
            self.image = pygame.transform.scale(self.image, (30, bottom))
            self.rect = self.image.get_rect(topleft=(WIDTH, 0))
        else:
            self.image = pygame.transform.scale(self.image, (30, HEIGHT - top))
            self.rect = self.image.get_rect(bottomleft=(WIDTH, HEIGHT))

        self.velocity = 2
        self.can_spawn_next = False

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= self.velocity
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
