import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PLAYER_SIZE = 30
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_WIDTH = 50
OBSTACLE_SPEED = 3
OBSTACLE_GAP_SIZE = 200
OBSTACLE_FREQUENCY = 60


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
        self.font = pygame.font.SysFont(None, 36)

        self.obstacle_timer = 0

    def spawn_obstacle(self):
        top_gap = random.randint(10, HEIGHT - OBSTACLE_GAP_SIZE - 10)
        bottom_gap = top_gap + OBSTACLE_GAP_SIZE
        top_obstacle = Obstacle(0, top_gap)
        bottom_obstacle = Obstacle(bottom_gap, HEIGHT)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.game_over = False

    def run(self, event):
        if not event:
            # No event has been passed
            return True

        if self.game_over:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True

        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.jump()

        self.all_sprites.update()
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.game_over = True

        self.obstacle_timer += 1
        if self.obstacle_timer >= OBSTACLE_FREQUENCY:
            self.obstacle_timer = 0
            self.spawn_obstacle()

        self.score += 1
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()
        self.clock.tick(FPS)
        return True


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.centery = HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        self.rect.y = max(self.rect.y, 0)
        self.rect.y = min(self.rect.y, HEIGHT - PLAYER_SIZE)

    def jump(self):
        self.velocity = JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, height):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = top

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if not event or event.type != pygame.QUIT:
            running = game.run(event)
        else:
            running = False
    pygame.quit()
