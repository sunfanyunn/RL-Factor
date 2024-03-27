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
        # Obstacle spawning implementation
        top_gap = random.randint(CAVERN_WIDTH // 2, HEIGHT - CAVERN_WIDTH * 1.5)
        bottom_gap = top_gap + CAVERN_WIDTH
        top_obstacle = Obstacle(bottom=top_gap)
        bottom_obstacle = Obstacle(top=bottom_gap)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        # Reset game implementation
        self.player.kill()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.player = Pixelcopter()
        self.all_sprites.add(self.player)
        self.score = 0
        self.game_over = False
        self.spawn_obstacle()

    def run(self, event):
        # Game loop implementation
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            self.player.jump()
        elif pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
            self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            # Spawn new obstacles as needed.
            for obstacle in self.obstacles:
                if not obstacle.spawned and obstacle.rect.right < WIDTH // 2:
                    obstacle.spawned = True
                    self.spawn_obstacle()

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                self.game_over = True
                self.display_game_over()

            self.score += 0.01  # Increase score as time passes
            score_text = f'Score: {int(self.score)}'
            text_surface = self.font.render(score_text, True, WHITE)
            self.screen.fill(BLACK)
            self.screen.blit(text_surface, (10, 10))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
        else:
            # Game over logic
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reset_game()

        self.clock.tick(FPS)
        return True

    def display_game_over(self):
        # Game over display implementation
        game_over_text = 'Game Over! Press Enter to Restart'
        text_surface = self.font.render(game_over_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        # Pixelcopter initialization implementation
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        # Pixelcopter update implementation
        self.velocity += 0.5  # Gravity
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        # Pixelcopter jump implementation
        self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        # Obstacle initialization implementation
        super().__init__()
        self.image = pygame.Surface((20, HEIGHT // 2))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(midbottom=(WIDTH, top))
        elif bottom is not None:
            self.rect = self.image.get_rect(midtop=(WIDTH, bottom))
        self.velocity = 2
        self.spawned = False

    def update(self):
        # Obstacle update implementation
        self.rect.x -= self.velocity
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.NOEVENT:
            continue
        running = game.run(event)
    pygame.quit()

