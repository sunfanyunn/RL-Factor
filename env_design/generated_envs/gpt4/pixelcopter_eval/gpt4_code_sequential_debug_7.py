import pygame
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1
JUMP_SPEED = -10
OBSTACLE_WIDTH = 50
OBSTACLE_SPEED = -2
COPTER_SIZE = 50

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

        self.font = pygame.font.SysFont(None, 72)
        self.score = 0
        self.last_obstacle = pygame.time.get_ticks()
        self.spawn_obstacle()

    def spawn_obstacle(self):
        top = random.randint(COPTER_SIZE * 2, HEIGHT // 2 - CAVERN_WIDTH // 2)
        bottom = top + CAVERN_WIDTH
        top_obstacle = Obstacle(bottom=top)
        bottom_obstacle = Obstacle(top=bottom)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.last_obstacle = pygame.time.get_ticks()

    def run(self, event):
        if event and event.type == pygame.QUIT:
            return False
        if self.game_over:
            if event and (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                self.reset_game()
        else:
            now = pygame.time.get_ticks()
            if now - self.last_obstacle > 1500:
                self.spawn_obstacle()
                self.last_obstacle = now

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump()
            if event and event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            self.screen.fill(BLACK)
            self.player.update(self.game_over)
            self.obstacles.update()
            self.all_sprites.draw(self.screen)

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                self.game_over = True

            for obstacle in self.obstacles:
                if obstacle.rect.right < self.player.rect.left and not getattr(obstacle, 'passed', False):
                    obstacle.passed = True
                    self.score += 0.5

            score_surf = self.font.render(f'Score: {int(self.score)}', True, WHITE)
            self.screen.blit(score_surf, (10, 10))

            if self.game_over:
                game_over_surf = self.font.render('Game Over!', True, WHITE)
                game_over_rect = game_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(game_over_surf, game_over_rect)

            pygame.display.flip()
            self.clock.tick(FPS)
        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((COPTER_SIZE, COPTER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0

    def update(self, game_over):
        if not game_over:
            self.velocity += GRAVITY
            self.rect.y += self.velocity
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    def jump(self):
        self.velocity = JUMP_SPEED

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        if top is not None:
            self.rect.bottom = top
        elif bottom is not None:
            self.rect.top = bottom

    def update(self):
        self.rect.x += OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        running = game.run(event)
    pygame.quit()

