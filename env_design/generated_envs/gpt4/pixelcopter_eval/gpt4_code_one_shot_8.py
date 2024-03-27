import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.spawn_obstacle()
        self.score = 0

    def spawn_obstacle(self):
        top_gap = random.randint(20, HEIGHT - 20 - CAVERN_WIDTH)
        bottom_gap = top_gap + CAVERN_WIDTH
        obstacle_top = Obstacle(bottom=bottom_gap)
        obstacle_bottom = Obstacle(top=top_gap)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.game_over = False
        self.player.rect.centery = HEIGHT // 2
        self.player.velocity = 0
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.spawn_obstacle()
        self.score = 0

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if not self.game_over:
            self.screen.fill(BLACK)
            self.all_sprites.update()
            self.spawn_obstacle()
            self.score += 1

            for obstacle in self.obstacles:
                if obstacle.rect.right < 0:
                    obstacle.kill()
            
            collisions = pygame.sprite.spritecollide(self.player, self.obstacles, False)
            if collisions or not 0 < self.player.rect.centery < HEIGHT:
                self.game_over = True

            self.all_sprites.draw(self.screen)
            self.display_score()
            pygame.display.flip()
        else:
            self.display_game_over()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.reset_game()
        self.clock.tick(FPS)
        return True

    def display_score(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(text, (10, 10))

    def display_game_over(self):
        font = pygame.font.SysFont(None, 72)
        text = font.render('Game Over!', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += 1
        self.rect.y += self.velocity
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.jump()

    def jump(self):
        self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((40, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(left=WIDTH)
        if top is not None:
            self.rect.bottom = top
        if bottom is not None:
            self.rect.top = bottom

    def update(self):
        self.rect.x -= 5


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
