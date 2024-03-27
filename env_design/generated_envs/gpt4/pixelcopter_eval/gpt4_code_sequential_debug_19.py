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

        self.font = pygame.font.SysFont(None, 36)
        self.score = 0

        self.spawn_obstacle()

    def spawn_obstacle(self):
        top = random.randint(50, HEIGHT // 2 - CAVERN_WIDTH // 2)
        bottom = top + CAVERN_WIDTH
        obstacle_top = Obstacle(top=top)
        obstacle_bottom = Obstacle(bottom=bottom)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.player.reset()
        self.obstacles.empty()
        self.score = 0
        self.all_sprites = pygame.sprite.Group(self.player)
        self.spawn_obstacle()
        self.game_over = False

    def run(self, event):
        if self.game_over:
            self.display_game_over()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()
            return True

        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.jump()

        self.all_sprites.update()
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
        if hits:
            self.game_over = True

        self.remove_passed_obstacles()
        self.score += 1 / FPS
        score_surface = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def remove_passed_obstacles(self):
        passed_obstacles = [obstacle for obstacle in self.obstacles if obstacle.rect.right < 0]
        for obstacle in passed_obstacles:
            obstacle.kill()
        if len(self.obstacles) < 4:
            self.spawn_obstacle()

    def display_game_over(self):
        game_over_surface = self.font.render('Game Over! Press R to restart', True, WHITE)
        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += 0.5  # gravity
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -10

    def reset(self):
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40
        self.moving_speed = 4
        if top is not None:
            height = top
            self.image = pygame.Surface((self.width, height))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect(topright=(WIDTH, 0))
        elif bottom is not None:
            height = HEIGHT - bottom
            self.image = pygame.Surface((self.width, height))
            self.image.fill(WHITE)
            y_coordinate = bottom
            self.rect = self.image.get_rect(topleft=(WIDTH, y_coordinate))

    def update(self):
        self.rect.x -= self.moving_speed


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT or not game.run(event):
            running = False
    pygame.quit()

