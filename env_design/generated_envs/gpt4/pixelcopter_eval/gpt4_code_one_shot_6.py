import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_SPEED = -5
SCORING_RATE = 100  # Points added to score for each frame survived


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.font = pygame.font.SysFont(None, 48)

    def spawn_obstacle(self):
        top_gap = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        bottom_gap = top_gap + CAVERN_WIDTH
        self.obstacles.add(Obstacle(bottom=bottom_gap), Obstacle(top=top_gap))
        for obstacle in self.obstacles:
            self.all_sprites.add(obstacle)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.spawn_obstacle()

    def run(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
            return True
        else:
            self.screen.fill(BLACK)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.bottom > HEIGHT or self.player.rect.top < 0:
                self.game_over = True
                game_over_text = self.font.render('Game Over!', True, WHITE)
                self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            else:
                self.score += SCORING_RATE // FPS
                score_text = self.font.render(str(self.score), True, WHITE)
                self.screen.blit(score_text, (10, 10))

                self.spawn_obstacle()

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
        self.rect.y += int(self.velocity)
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity = 0
        elif self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        if top:
            self.image = pygame.Surface((20, top))
            self.rect = self.image.get_rect(topright=(WIDTH, 0))
        elif bottom:
            self.image = pygame.Surface((20, HEIGHT - bottom))
            self.rect = self.image.get_rect(bottomright=(WIDTH, HEIGHT))
        self.image.fill(WHITE)

    def update(self):
        self.rect.x += OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            game.player.jump()
        running = game.run(event)
    pygame.quit()
