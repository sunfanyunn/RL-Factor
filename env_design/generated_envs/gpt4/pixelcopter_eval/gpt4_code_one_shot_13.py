import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_WIDTH = 50
OBSTACLE_SPEED = 5
OBSTACLE_GAP_SIZE = 200
obstacle_frequency = set_obstacle_freq(FPS)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        top = random.randint(50, HEIGHT - OBSTACLE_GAP_SIZE - 50)
        bottom = top + OBSTACLE_GAP_SIZE

        obstacle_top = Obstacle(bottom=bottom)
        obstacle_bottom = Obstacle(top=top)

        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(self.obstacles)

    def reset_game(self):
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_obstacle()
        self.score = 0
        self.game_over = False

    def check_collision(self):
        if pygame.sprite.spritecollide(self.player, self.obstacles, False) or not 0 < self.player.rect.y < HEIGHT:
            self.game_over = True

    def run(self, event):
        while not self.game_over:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.player.jump()

            self.check_collision()
            if not self.game_over:
                self.all_sprites.update()

                if len(self.obstacles) < 6:
                    self.spawn_obstacle()

                self.screen.fill(BLACK)
                self.all_sprites.draw(self.screen)

                pygame.display.flip()
            else:
                self.display_game_over()

            self.score += 1

    def display_game_over(self):
        font = pygame.font.SysFont(None, 74)
        text = font.render('Game Over!', True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        self.reset_game()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)

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
        self.velocity = JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        if top is None and bottom is None:
            middle = HEIGHT / 2
            top, bottom = middle - CAVERN_WIDTH / 2, middle + CAVERN_WIDTH / 2

        if top is not None:
            self.rect = self.image.get_rect(bottom=top)
        elif bottom is not None:
            self.rect = self.image.get_rect(top=bottom)
        self.rect.x = WIDTH

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()


# Utility function to determine obstacle spawn frequency based on FPS
# Provides a function that can be used for unit testing

def set_obstacle_freq(FPS):
    return max(1, 2 * FPS)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        game.run(event)
    pygame.quit()
