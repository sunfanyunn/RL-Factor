import pygame
import random

# Define the display's width and height
WIDTH, HEIGHT = 640, 480
FPS = 60

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PLAYER_SIZE = 50
PLAYER_JUMP_FORCE = 10
GRAVITY = 1
OBSTACLE_WIDTH = 70
OBSTACLE_SPEED = -5
OBSTACLE_SPACING = 300
CAVERN_WIDTH = 100


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

        self.spawn_obstacle()
        self.score = 0

    def spawn_obstacle(self):
        obstacle_gap = random.randint(50, HEIGHT - CAVERN_WIDTH - 50)
        top_obstacle = Obstacle(0, obstacle_gap)
        bottom_obstacle = Obstacle(obstacle_gap + CAVERN_WIDTH, HEIGHT)

        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

        for obstacle in self.obstacles:
            if obstacle.rect.right < WIDTH:
                obstacle.rect.x = WIDTH + OBSTACLE_WIDTH
            else:
                obstacle.rect.x = self.obstacles.sprites()[-1].rect.right + OBSTACLE_SPACING

    def reset_game(self):
        self.player.reset()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.spawn_obstacle()
        self.score = 0
        self.game_over = False

    def run(self, event):
        if not self.game_over:
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_UP]:
                self.player.jump()

            self.all_sprites.update()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            self.score += 1
            score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT:
                self.game_over = True
        else:
            game_over_text = pygame.font.SysFont(None, 48).render('Game Over!', True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(game_over_text, game_over_rect)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(FPS)
        return not self.game_over


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super(Pixelcopter, self).__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def jump(self):
        self.velocity = -PLAYER_JUMP_FORCE

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.game_over = True

    def reset(self):
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        super(Obstacle, self).__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, bottom - top))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = WIDTH

    def update(self):
        self.rect.x += OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            running = game.run(event)
    pygame.quit()
