
import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 1
JUMP_STRENGTH = -20
SPEED = 5


class Game:
    def __init__(self):
        pygame.display.set_caption("Pixelcopter Game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        
        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        self.spawn_obstacle()

        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def spawn_obstacle(self):
        top = random.randint(0, HEIGHT - CAVERN_WIDTH)
        bottom = top + CAVERN_WIDTH
        
        obstacle_top = Obstacle(bottom=bottom)
        obstacle_bottom = Obstacle(top=top)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)
    
    def reset_game(self):
        self.game_over = False
        self.player.kill()
        for obstacle in self.obstacles:
            obstacle.kill()
        self.player = Pixelcopter()
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.spawn_obstacle()
        self.score = 0

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            self.screen.fill(BLACK)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            if pygame.sprite.spritecollideany(self.player, self.obstacles) or not self.screen.get_rect().contains(self.player.rect):
                self.game_over = True

            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if self.obstacles.sprites()[-1].rect.right < WIDTH:
                self.spawn_obstacle()

            for obstacle in self.obstacles:
                if obstacle.rect.right < 0:
                    obstacle.kill()
                    self.score += 1

            pygame.display.flip()

        else:
            game_over_text = self.font.render("Game Over!", True, WHITE)
            restart_text = self.font.render("Click to restart", True, WHITE)
            self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 50))
            self.screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, HEIGHT // 2))
            pygame.display.flip()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()

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
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        width = 40
        self.image = pygame.Surface((width, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(right=WIDTH)

        if top is not None:
            self.rect.top = 0
            self.rect.height = top
        if bottom is not None:
            self.rect.bottom = HEIGHT
            self.rect.height = HEIGHT - bottom

    def update(self):
        self.rect.x -= SPEED


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

