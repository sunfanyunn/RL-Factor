import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
OBSTACLE_INTERVAL = 100  # The interval at which to spawn obstacles


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

        self.score_font = pygame.font.Font(None, 36)
        self.score = 0
        self.obstacle_timer = 0
        self.spawn_obstacle()

    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top = random.randint(20, HEIGHT // 2 - CAVERN_WIDTH // 2)
        bottom = top + CAVERN_WIDTH
        obstacle_top = Obstacle(bottom=top)
        obstacle_bottom = Obstacle(top=bottom)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

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
        self.obstacle_timer = 0
        self.spawn_obstacle()

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        if event.type == pygame.QUIT:
            return False

        mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)
        if not self.game_over:
            if mouse_clicked:
                self.player.jump()

            self.player.update()
            self.obstacles.update()

            self.obstacle_timer += 1
            if self.obstacle_timer >= OBSTACLE_INTERVAL:
                self.spawn_obstacle()
                self.obstacle_timer = 0

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                self.game_over = True
            else:
                self.score += 1

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.display_score()
            pygame.display.flip()
            self.clock.tick(FPS)
        else:
            self.display_game_over()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
        return True

    def display_game_over(self):
        game_over_text = self.score_font.render('Game Over! Press R to restart.', True, WHITE)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()  # Ensure the game over text is displayed

    def display_score(self):
        score_text = self.score_font.render('Score: ' + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))


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
        self.velocity += 0.5  # simulate gravity
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

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
        self.image = pygame.Surface((40, HEIGHT // 2))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(midbottom=(WIDTH, top))
        elif bottom is not None:
            self.rect = self.image.get_rect(midtop=(WIDTH, bottom))

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= 2
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

