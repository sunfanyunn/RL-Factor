import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1.0
JUMP_STRENGTH = -10.0
OBSTACLE_SPEED = 5
OBSTACLE_FREQUENCY = 90  # Higher value = less frequent


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PixelCopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.player = PixelCopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def spawn_obstacle(self):
        # Randomly create a gap somewhere along the height
        gap_top = random.randint(0, HEIGHT - CAVERN_WIDTH)
        gap_bottom = gap_top + CAVERN_WIDTH
        # Create two obstacles for the top and bottom
        top_obstacle = Obstacle(bottom=gap_top)
        bottom_obstacle = Obstacle(top=gap_bottom)

        # Add the obstacles to the relevant groups
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.player = PixelCopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if self.game_over:
            self.display_game_over()
            # Restart the game if the player presses a key or clicks
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.reset_game()
            return True

        # Check for jump
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self.player.jump()

        # Spawn obstacles
        if pygame.time.get_ticks() % OBSTACLE_FREQUENCY == 0:
            self.spawn_obstacle()

        # Update all the sprites
        self.all_sprites.update()

        # Check for collisions
        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over = True
        if self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
            self.game_over = True

        # Move and delete obstacles
        for obstacle in self.obstacles:
            if obstacle.rect.right < 0:
                obstacle.kill()

        self.score += 1

        # Draw everything
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # Show score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def display_game_over(self):
        game_over_text = self.font.render("Game Over!", True, WHITE)
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
        pygame.display.flip()


class PixelCopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH//4, HEIGHT//2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((20, HEIGHT))
        self.image.fill(WHITE)

        if top is not None:
            self.rect = self.image.get_rect(bottomleft=(WIDTH, top))
        elif bottom is not None:
            self.rect = self.image.get_rect(topleft=(WIDTH, bottom))

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
