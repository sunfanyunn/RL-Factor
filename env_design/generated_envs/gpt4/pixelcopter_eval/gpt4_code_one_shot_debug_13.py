import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_WIDTH = 50
OBSTACLE_SPEED = 5
OBSTACLE_GAP_SIZE = 150
CAVERN_WIDTH = 100


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0

        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        top = random.randint(50, HEIGHT - OBSTACLE_GAP_SIZE - 50)
        bottom = top + OBSTACLE_GAP_SIZE

        obstacle_top = Obstacle(bottom=top)
        obstacle_bottom = Obstacle(top=bottom)

        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.player = Pixelcopter()
        self.obstacles.empty()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.score = 0
        self.game_over = False
        self.spawn_obstacle()

    def check_collision(self):
        if pygame.sprite.spritecollide(self.player, self.obstacles, False) or not 0 <= self.player.rect.y <= HEIGHT:
            self.game_over = True

    def run(self, event):
        self.clock.tick(FPS)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.player.jump()

        if not self.game_over:
            self.check_collision()
            self.all_sprites.update()
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            obstacle_list = self.obstacles.sprites()
            for obstacle in obstacle_list:
                if obstacle.rect.x < -OBSTACLE_WIDTH:
                    obstacle.kill()
            if not self.obstacles or (obstacle_list[-1].rect.x < WIDTH - 300):
                self.spawn_obstacle()

            font = pygame.font.SysFont(None, 36)
            text = font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(text, (10, 10))

            pygame.display.flip()
            self.score += 1
        else:
            self.display_game_over()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()

        return not self.game_over

    def display_game_over(self):
        font = pygame.font.SysFont(None, 74)
        text = font.render('Game Over!', True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
    

class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)

        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        if self.rect.bottom < HEIGHT:
            self.velocity = JUMP_STRENGTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT))

        if top is not None:
            self.image.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            self.rect = self.image.get_rect(topright=(WIDTH + OBSTACLE_WIDTH, 0))
            self.rect.height = top
        elif bottom is not None:
            self.image.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            self.rect = self.image.get_rect(topleft=(WIDTH + OBSTACLE_WIDTH, bottom))

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
        running = game.run(event)
    pygame.quit()