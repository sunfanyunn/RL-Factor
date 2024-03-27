import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1
JUMP_STRENGTH = 10
OBSTACLE_WIDTH = 30
OBSTACLE_SPEED = 5
OBSTACLE_GAP_SIZE = 200
OBSTACLE_FREQUENCY = 90


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.obstacle_timer = 0

    def spawn_obstacle(self):
        top_gap = random.randint(50, HEIGHT - OBSTACLE_GAP_SIZE - 50)
        bottom_gap = top_gap + OBSTACLE_GAP_SIZE
        top_obstacle = Obstacle(0, top_gap)
        bottom_obstacle = Obstacle(bottom_gap, HEIGHT)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.player.jump()

        if not self.game_over:
            self.screen.fill(BLACK)

            self.player.update()
            self.obstacles.update()
            self.obstacle_timer += 1
            if self.obstacle_timer > OBSTACLE_FREQUENCY:
                self.obstacle_timer = 0
                self.spawn_obstacle()

            self.all_sprites.draw(self.screen)

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or not self.screen.get_rect().contains(self.player.rect):
                self.game_over = True

            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

            self.score += 1
        else:
            game_over_text = self.font.render("Game Over!", True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            restart_text = self.font.render("Click to restart", True, WHITE)
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2 + 50))

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -JUMP_STRENGTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, bottom - top))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        if top == 0:
            self.rect.top = 0
        else:
            self.rect.bottom = top
        self.rect.right = WIDTH

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
