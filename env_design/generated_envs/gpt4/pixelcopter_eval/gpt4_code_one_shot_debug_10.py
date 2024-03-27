import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GRAVITY = 0.5
JUMP_STRENGTH = 10
OBSTACLE_WIDTH = 50
OBSTACLE_SPEED = 2
OBSTACLE_GAP_SIZE = 200
OBSTACLE_FREQUENCY = 90


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.score = 0
        self.font = pygame.font.Font(None, 36)

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.obstacle_timer = 0

    def spawn_obstacle(self):
        top_height = random.randint(50, HEIGHT - OBSTACLE_GAP_SIZE - 50)
        bottom_height = HEIGHT - top_height - OBSTACLE_GAP_SIZE
        top_obstacle = Obstacle(0, top_height)
        bottom_obstacle = Obstacle(top_height + OBSTACLE_GAP_SIZE, HEIGHT - top_height - OBSTACLE_GAP_SIZE)
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
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

        self.screen.fill(BLACK)

        if not self.game_over:
            self.player.update()
            self.obstacles.update()

        self.all_sprites.draw(self.screen)

        if not self.game_over:
            self.obstacle_timer += 1
            if self.obstacle_timer >= OBSTACLE_FREQUENCY:
                self.obstacle_timer = 0
                self.spawn_obstacle()

            self.score += 1

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if pygame.sprite.spritecollide(self.player, self.obstacles, False) or not self.screen.get_rect().contains(self.player.rect):
            self.game_over = True

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            restart_text = self.font.render('Click to restart', True, WHITE)
            self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 3))
            self.screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, (HEIGHT // 3) * 2))
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(FPS)
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, height):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = WIDTH

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
