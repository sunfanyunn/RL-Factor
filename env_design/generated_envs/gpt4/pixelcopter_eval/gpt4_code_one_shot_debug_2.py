import pygame
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PLAYER_SIZE = 50
GRAVITY = 0.5
THRUST = -10
CAVERN_WIDTH = 100  # Width of the gap in the cavern
OBSTACLE_WIDTH = 70
OBSTACLE_SPEED = 3
SPAWN_INTERVAL = 1500

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
        self.font = pygame.font.Font(None, 36)
        self.spawn_timer = pygame.time.get_ticks()

    def spawn_obstacle(self):
        top_height = random.randint(50, HEIGHT // 2)
        bottom_height = top_height + CAVERN_WIDTH

        obstacle_top = Obstacle(top=top_height - OBSTACLE_WIDTH, bottom=top_height)
        obstacle_bottom = Obstacle(top=bottom_height, bottom=HEIGHT)

        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.game_over = False
        self.score = 0
        self.spawn_timer = pygame.time.get_ticks()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_timer > SPAWN_INTERVAL:
                self.spawn_timer = current_time
                self.spawn_obstacle()

            self.all_sprites.update()
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.score += 1
            score_text = self.font.render(str(self.score), True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if pygame.sprite.spritecollide(self.player, self.obstacles, False):
                self.game_over = True

        else:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, 
                                              (HEIGHT - game_over_text.get_height()) // 2))
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

        pygame.display.update()
        self.clock.tick(FPS)

        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
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

    def jump(self):
        self.velocity = THRUST

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((OBSTACLE_WIDTH, bottom - top))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        if top == 0:
            self.rect.top = 0
        else:
            self.rect.bottom = top

    def update(self):
        self.rect.x -= OBSTACLE_SPEED

        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
