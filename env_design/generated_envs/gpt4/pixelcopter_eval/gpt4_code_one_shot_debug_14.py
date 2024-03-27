import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAVITY = 1
FLY_SPEED = -15
OBSTACLE_WIDTH = 30
OBSTACLE_GAP_SIZE = 200
OBSTACLE_SPEED = 5
CAVERN_WIDTH = 100

pygame.init()
SCORE_FONT = pygame.font.Font(None, 36)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.spawn_obstacle()

    def spawn_obstacle(self):
        top = random.randint(CAVERN_WIDTH, HEIGHT - OBSTACLE_GAP_SIZE - CAVERN_WIDTH)
        bottom = top + OBSTACLE_GAP_SIZE
        obstacle_top = Obstacle(top=top)
        obstacle_bottom = Obstacle(bottom=bottom)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.spawn_obstacle()
        self.game_over = False

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        if not self.game_over:
            if keys[pygame.K_SPACE] or mouse_pressed[0]:
                self.player.jump()

            self.all_sprites.update()

            hits = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if hits or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                self.game_over = True

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.score += 1
            score_text = SCORE_FONT.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            for obstacle in self.obstacles:
                if obstacle.rect.right < 0:
                    obstacle.kill()
            if not any(obstacle.rect.right >= WIDTH for obstacle in self.obstacles):
                self.spawn_obstacle()
        else:
            game_over_text = SCORE_FONT.render('Game Over!', True, WHITE)
            self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) / 2, (HEIGHT - game_over_text.get_height()) / 2))
            if keys[pygame.K_SPACE] or mouse_pressed[0]:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = FLY_SPEED

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))
        self.image.fill(WHITE)
        if top is not None:
            self.rect = self.image.get_rect(top=top - HEIGHT, right=WIDTH)
        elif bottom is not None:
            self.rect = self.image.get_rect(bottom=bottom, right=WIDTH)

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
