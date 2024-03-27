import pygame
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern


class Game:
    def __init__(self):
        pygame.init()
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
        gap_y = random.randint(100, HEIGHT - 100)
        top_obstacle = Obstacle(bottom=gap_y - (CAVERN_WIDTH // 2))
        bottom_obstacle = Obstacle(top=gap_y + (CAVERN_WIDTH // 2))
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.player = Pixelcopter()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.obstacles.empty()
        self.score = 0
        self.spawn_obstacle()

    def run(self, event):
        if self.game_over:
            self.screen.fill(BLACK)
            game_over_text = self.font.render('Game Over! Press Space to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            pygame.display.flip()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()
        else:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            self.screen.fill(BLACK)
            self.all_sprites.update()

            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True

            if not self.game_over:
                self.score += 1

            for obstacle in list(self.obstacles):
                if obstacle.rect.right < 0:
                    obstacle.kill()

            if len(self.obstacles) < 4:
                self.spawn_obstacle()

            for entity in self.all_sprites:
                self.screen.blit(entity.image, entity.rect)

            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(FPS)

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super(Pixelcopter, self).__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += 1  # gravity effect
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -10

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super(Obstacle, self).__init__()
        width = random.randint(20, 40)
        self.image = pygame.Surface((width, HEIGHT))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(bottomleft=(WIDTH, top))
        else:
            self.rect = self.image.get_rect(topleft=(WIDTH, bottom))

    def update(self):
        self.rect.x -= 2

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()

