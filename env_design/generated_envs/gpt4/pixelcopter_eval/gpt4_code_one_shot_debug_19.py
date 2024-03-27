import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAVITY = 0.5
THRUST = -10
CAVERN_WIDTH = 100
OBSTACLE_WIDTH = 50
OBSTACLE_GAP_SIZE = 200
OBSTACLE_FREQUENCY = 1500


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

        pygame.time.set_timer(pygame.USEREVENT, OBSTACLE_FREQUENCY)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        top = random.randint(CAVERN_WIDTH, HEIGHT - CAVERN_WIDTH - OBSTACLE_GAP_SIZE)
        bottom = top + OBSTACLE_GAP_SIZE
        obstacle_top = Obstacle(top=0, bottom=top)
        obstacle_bottom = Obstacle(top=bottom, bottom=HEIGHT)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.game_over = False
        self.player.kill()
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.score = 0
        self.spawn_obstacle()

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.USEREVENT:
                    self.spawn_obstacle()
                self.player.handle_event(event)

            self.screen.fill(BLACK)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if hits:
                self.game_over = True

            self.score += 1
            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(FPS)

        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                    return True

            score_text = self.font.render('Game Over! Press R to Restart', True, WHITE)
            self.screen.blit(score_text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super(Pixelcopter, self).__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.velocity = THRUST

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super(Obstacle, self).__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, bottom - top))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        if top == 0:
            self.rect.bottom = bottom
        else:
            self.rect.top = top

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
