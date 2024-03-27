import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
OBSTACLE_WIDTH = 50
OBSTACLE_SPEED = 3
GRAVITY = 1
JUMP_SPEED = -10


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_obstacle()
        self.score = 0

    def spawn_obstacle(self):
        top_height = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        bottom_height = top_height + CAVERN_WIDTH

        top_obstacle = Obstacle(0, top_height)
        bottom_obstacle = Obstacle(bottom_height, HEIGHT)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_obstacle()
        self.player.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.player.velocity = 0
        self.game_over = False
        self.score = 0

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if self.game_over:
            if event.type == pygame.KEYDOWN:
                self.reset_game()
            return True

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            self.player.jump()

        self.screen.fill(BLACK)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

        # Check if player hits a boundary or an obstacle
        if self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT or 
           pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over = True
            self.display_message("Game Over!", 48, WIDTH // 2, HEIGHT // 2)

        if not self.game_over:
            # Move and spawn new obstacles
            for obstacle in list(self.obstacles):
                if obstacle.rect.right < 0:
                    self.obstacles.remove(obstacle)
                    self.all_sprites.remove(obstacle)
                    self.score += 1
                    self.spawn_obstacle()

            # Display the current score
            self.display_message(f"Score: {self.score}", 32, 80, 20)

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

    def display_message(self, text, size, x, y):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_SPEED


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, bottom - top))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(right=WIDTH, top=top)

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
