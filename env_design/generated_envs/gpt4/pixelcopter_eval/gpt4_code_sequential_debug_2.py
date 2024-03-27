import pygame
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
        self.all_sprites = pygame.sprite.Group(self.player)

        self.score = 0
        self.score_font = pygame.font.SysFont('arial', 32)
        self.spawn_obstacle()

    def spawn_obstacle(self):
        gap_y = random.randint(120, HEIGHT - 120)
        top_obstacle = Obstacle(top=-1, bottom=gap_y - CAVERN_WIDTH // 2)
        bottom_obstacle = Obstacle(top=gap_y + CAVERN_WIDTH // 2, bottom=HEIGHT + 1)
        self.obstacles.add(top_obstacle, bottom_obstacle)
        self.all_sprites.add(top_obstacle, bottom_obstacle)

    def reset_game(self):
        self.game_over = False
        self.player.rect.y = HEIGHT // 2
        self.player.velocity = 0
        self.score = 0

        for obstacle in self.obstacles:
            obstacle.kill()

        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and self.game_over:
            self.reset_game()

        self.all_sprites.update()
        self.screen.fill(BLACK)

        if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
            if not self.game_over:
                self.game_over = True
                self.display_game_over()
        else:
            self.score += 1
            score_text = self.score_font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if len(self.obstacles) < 2:  # Ensuring there are always obstacles
                self.spawn_obstacle()

        if not self.game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            self.player.jump()

        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def display_game_over(self):
        game_over_text = self.score_font.render('Game Over!', True, WHITE)
        start_text = self.score_font.render('Click to restart', True, WHITE)
        self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
        self.screen.blit(start_text, ((WIDTH - start_text.get_width()) // 2, (HEIGHT - start_text.get_height()) // 2 + 50))
        pygame.display.flip()
        self.clock.tick(FPS)


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        if not self.rect.top < 0 and not self.rect.bottom > HEIGHT:
            self.velocity += 0.5
        self.rect.y += int(self.velocity)

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        if not self.rect.top < 0:
            self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom):
        super().__init__()
        self.image = pygame.Surface((30, HEIGHT // 2 - CAVERN_WIDTH // 2))
        self.image.fill(WHITE)
        if top != -1:
            self.rect = self.image.get_rect(topleft=(WIDTH, top - (HEIGHT // 2 - CAVERN_WIDTH // 2)))
        elif bottom != HEIGHT + 1:
            self.rect = self.image.get_rect(bottomleft=(WIDTH, bottom))

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.NOEVENT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if not running:
                break
            game.all_sprites.update()
            game.screen.fill(BLACK)
            game.all_sprites.draw(game.screen)
            pygame.display.flip()
            game.clock.tick(FPS)
        else:
            running = game.run(event)
    pygame.quit()
