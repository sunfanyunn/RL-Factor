import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GRAVITY = 1
JUMP_STRENGTH = 10
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
        self.font = pygame.font.SysFont(None, 36)

        self.score = 0

        self.spawn_obstacle()

    def spawn_obstacle(self):
        bottom = random.randint(int(HEIGHT / 2), HEIGHT)
        top = bottom - CAVERN_WIDTH
        obstacle_top = Obstacle(bottom=top)
        obstacle_bottom = Obstacle(top=bottom)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.player.kill()
        for obstacle in self.obstacles:
            obstacle.kill()

        self.player = Pixelcopter()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.obstacles = pygame.sprite.Group()
        self.score = 0
        self.game_over = False

        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if self.game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            self.reset_game()

        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            self.all_sprites.update()

            for obstacle in self.obstacles:
                obstacle.update()

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT:
                self.game_over = True

            self.score += 1

        self.screen.fill(BLACK)
        if self.game_over:
            game_over_message = self.font.render('Game Over!', True, WHITE)
            self.screen.blit(game_over_message, (WIDTH // 2 - game_over_message.get_width() // 2, HEIGHT // 2 - game_over_message.get_height() // 2))
        else:
            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)

        if len(self.obstacles) < 6:
            self.spawn_obstacle()

        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH / 4, HEIGHT / 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        if self.rect.bottom != HEIGHT:  # This condition prevents the copter from jumping when it is on the ground
            self.velocity = -JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((20, HEIGHT))
        self.image.fill(WHITE)
        if bottom is not None:
            self.rect = self.image.get_rect(topleft=(WIDTH, bottom))
        elif top is not None:
            self.rect = self.image.get_rect(bottomleft=(WIDTH, top))

    def update(self):
        self.rect.x -= 2
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
            if not game.game_over or event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = game.run(event)
    pygame.quit()
