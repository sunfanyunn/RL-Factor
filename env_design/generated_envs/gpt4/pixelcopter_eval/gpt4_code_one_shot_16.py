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
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0

    def run(self, event):
        """
        Run the game loop
        event is the current Pygame event
        Returns False if the game should exit, True otherwise
        """
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            self.screen.fill(BLACK)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump()
            if pygame.mouse.get_pressed()[0]:
                self.player.jump()

            self.player.update()
            self.obstacles.update()

            self.score += 1
            score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            for obstacle in self.obstacles:
                if obstacle.rect.right < 0:
                    self.obstacles.remove(obstacle)
                    self.all_sprites.remove(obstacle)
                    self.spawn_obstacle()

            self.all_sprites.draw(self.screen)

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or not 0 <= self.player.rect.y <= HEIGHT:
                self.game_over = True
                message = pygame.font.SysFont(None, 48).render('Game Over!', True, WHITE)
                self.screen.blit(message, (WIDTH//2 - message.get_width()//2, HEIGHT//2 - message.get_height()//2))

            pygame.display.flip()

        else:
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN)):
                self.reset_game()

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
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.velocity = 0

    def update(self):
        """
        Update the Pixelcopter's position
        """
        self.velocity += 0.5  # Gravity
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        """
        Make the Pixelcopter jump
        """
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
        self.image = pygame.Surface((30, HEIGHT))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(topright=(WIDTH, 0))
            self.image = self.image.subsurface(pygame.Rect(0, 0, 30, top))
        if bottom is not None:
            self.rect = self.image.get_rect(bottomright=(WIDTH, HEIGHT))
            self.image = self.image.subsurface(pygame.Rect(0, bottom, 30, HEIGHT - bottom))

    def update(self):
        """
        Update the obstacle's position
        """
        self.rect.x -= 5


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    game.spawn_obstacle()  # Start by spawning the first obstacle
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
