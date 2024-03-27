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
        self.spawn_obstacle()

        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        
    def spawn_obstacle(self):
        """
        Spawn obstacles in the game world
        """
        top = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        bottom = top + CAVERN_WIDTH
        new_obstacle = Obstacle(top, bottom)
        self.obstacles.add(new_obstacle)
        self.all_sprites.add(new_obstacle)

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
        self.spawn_obstacle()

    def update_score(self):
        text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(text, (10, 10))

    def run(self):
        """
        Run the game loop
        Returns False if the game should exit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if not self.game_over and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            if not self.obstacles or self.obstacles.sprites()[-1].rect.right < WIDTH - 200:
                self.spawn_obstacle()
            self.score = self.player.rect.right // 200

            if pygame.sprite.spritecollideany(self.player, self.obstacles) or self.player.is_off_screen():
                self.game_over = True
                font = pygame.font.SysFont(None, 74)
                text = font.render('Game Over!', True, WHITE)
                text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                self.screen.fill(BLACK)
                self.screen.blit(text, text_rect)
                pygame.display.flip()

                # Ensure game runs at the correct framerate
                self.clock.tick(FPS)
            else:
                self.screen.fill(BLACK)
                self.all_sprites.draw(self.screen)
                self.update_score()
                pygame.display.flip()

                # Ensure game runs at the correct framerate
                self.clock.tick(FPS)
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()

        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0
    
    def update(self):
        self.velocity += 1  # Apply gravity
        self.rect.y += self.velocity

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.kill()

    def is_off_screen(self):
        return self.rect.top < 0 or self.rect.bottom > HEIGHT

    def jump(self):
        self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        width = random.randint(20, 60)
        self.image = pygame.Surface((width, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        if top is not None and bottom is not None:
            gap = pygame.Surface((width, bottom - top))
            gap.fill(BLACK)
            self.image.blit(gap, (0, top))
        self.velocity = -3

    def update(self):
        self.rect.x += self.velocity
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
