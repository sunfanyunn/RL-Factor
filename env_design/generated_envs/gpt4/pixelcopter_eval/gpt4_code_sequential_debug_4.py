import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern


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
        self.font = pygame.font.Font(None, 36)
        pygame.time.set_timer(pygame.USEREVENT+1, 1500)

    def spawn_obstacle(self):
        new_obstacle = Obstacle()
        self.obstacles.add(new_obstacle)
        self.all_sprites.add(new_obstacle)
        self.all_sprites.add(new_obstacle.partner)

    def reset_game(self):
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.score = 0
        self.game_over = False

    def run(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.reset_game()
            return True
        else:
            self.screen.fill(BLACK)
            self.all_sprites.update()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN:
                self.player.jump()

            for entity in self.all_sprites:
                self.screen.blit(entity.image, entity.rect)

            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top <= 0 or self.player.rect.bottom >= HEIGHT:
                self.game_over = True

            if not self.game_over:
                self.increment_score()

            if self.game_over:
                game_over_text = self.font.render('Game Over! Click to Play Again!', True, WHITE)
                text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(game_over_text, text_rect)

            pygame.display.flip()

        self.clock.tick(FPS)
        return True

    def increment_score(self):
        self.score += 1


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH / 4, HEIGHT / 2))
        self.velocity = 0

    def update(self):
        self.velocity += 0.5  # Gravity
        if (self.rect.y >= 0 or self.velocity > 0) and (self.rect.bottom <= HEIGHT or self.velocity < 0):
            self.rect.y += int(self.velocity)

    def jump(self):
        if self.rect.bottom < HEIGHT:
            self.velocity = -10


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        top = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        self.image = pygame.Surface((30, HEIGHT - top - CAVERN_WIDTH))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midtop=(WIDTH, top + CAVERN_WIDTH))

        self.partner = pygame.sprite.Sprite()
        self.partner.image = pygame.Surface((30, top))
        self.partner.image.fill(WHITE)
        self.partner.rect = self.partner.image.get_rect(midbottom=(WIDTH, top))

    def update(self):
        self.rect.x -= 2
        self.partner.rect.x -= 2

        if self.rect.right < 0:
            self.kill()
            self.partner.kill()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT+1:
            game.spawn_obstacle()
        running = game.run(event)
    pygame.quit()

