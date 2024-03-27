import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60
GRAVITY = 0.5
FLAP_POWER = -10
OBSTACLE_WIDTH = 70
OBSTACLE_SPEED = 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CAVERN_WIDTH = 100

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.player = Pixelcopter(self)
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.spawn_obstacle()

    def spawn_obstacle(self):
        top_gap = random.randint(50, HEIGHT - CAVERN_WIDTH - 50)
        bottom_gap = top_gap + CAVERN_WIDTH
        top_obstacle = Obstacle(bottom=top_gap)
        bottom_obstacle = Obstacle(top=bottom_gap)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.player.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.player.velocity = 0
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.score = 0
        self.spawn_obstacle()

    def run(self, event):
        self.screen.fill(BLACK)

        if not self.game_over:
            self.player.update()
            self.obstacles.update()
            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True
            for obstacle in self.obstacles:
                if obstacle.rect.right < 0:
                    obstacle.kill()
                    self.score += 0.5
            if len(self.obstacles) < 2:
                self.spawn_obstacle()

        else:
            game_over_text = self.font.render('Game Over! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.jump()
            elif event.key == pygame.K_r and self.game_over:
                self.reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            self.player.jump()

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.game.game_over = True

    def jump(self):
        self.velocity = FLAP_POWER

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        self.image.fill(BLACK)
        if top is not None:
            self.rect = self.image.get_rect(right=WIDTH, top=0)
            self.image.set_colorkey(BLACK)
            pygame.draw.rect(self.image, WHITE, [0, 0, OBSTACLE_WIDTH, top])
        if bottom is not None:
            self.rect = self.image.get_rect(right=WIDTH, top=bottom)
            self.image.set_colorkey(BLACK)
            pygame.draw.rect(self.image, WHITE, [0, bottom, OBSTACLE_WIDTH, HEIGHT-bottom])

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
