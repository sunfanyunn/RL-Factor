import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GRAVITY = 1
JUMP_STRENGTH = 10
CAVERN_WIDTH = 100  # Width of the gap in the cavern


class Game:
    def __init__(self):
        pygame.display.set_caption("Pixelcopter Game")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        bottom = random.randint(int(HEIGHT / 2), HEIGHT - 50)
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
        self.spawn_obstacle()

        self.score = 0
        self.game_over = False

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()

        if not self.game_over:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if keys[pygame.K_SPACE] or keys[pygame.K_UP] or event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.jump()
            self.all_sprites.update()
            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT:
                self.game_over = True
                game_over_message = self.font.render('Game Over!', True, WHITE)
                self.screen.blit(game_over_message, (WIDTH / 2 - 50, HEIGHT / 2))
                pygame.display.flip()
                pygame.time.delay(2000)
                self.reset_game()
            else:
                self.score += 1
        else:
            self.reset_game()

        self.screen.fill(BLACK)

        score_text = self.font.render('Score: ' + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()

        self.clock.tick(FPS)
        return True

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super(Pixelcopter, self).__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH / 4, HEIGHT / 2))
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
        self.velocity = -JUMP_STRENGTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super(Obstacle, self).__init__()
        self.image = pygame.Surface((20, HEIGHT))
        self.image.fill(WHITE)
        if top:
            self.rect = self.image.get_rect(bottomleft=(WIDTH, top))
        else:
            self.rect = self.image.get_rect(topleft=(WIDTH, bottom))

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
