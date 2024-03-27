import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
OBS_WIDTH = 40
OBS_GAP = 200  # Gap between obstacles
OBS_SPEED = -4  # Speed at which the obstacles move


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

        self.font = pygame.font.Font(None, 36)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        gap_top = random.randint(50, HEIGHT - 50 - CAVERN_WIDTH)
        Obstacle.create_pair(self, WIDTH, gap_top, gap_top + CAVERN_WIDTH)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.player.reset()

        for obs in list(self.obstacles):
            obs.kill()

        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if not self.game_over:
            self.handle_input(event)
            self.all_sprites.update()
            self.update_obstacles()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if self.player.check_collision(self.obstacles) or self.player.check_boundaries():
                self.game_over = True
                self.show_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)
        else:
            self.handle_game_over(event)
        
        return not self.game_over

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.player.jump()

    def update_obstacles(self):
        last_obstacle = None
        for obstacle in list(self.obstacles):
            obstacle.rect.x += OBS_SPEED
            if obstacle.rect.right < 0:
                obstacle.kill()
                self.score += 1  # Increment score when an obstacle passes

            if last_obstacle is None or WIDTH - last_obstacle.rect.right >= OBS_GAP:
                last_obstacle = obstacle
        
        if last_obstacle and WIDTH - last_obstacle.rect.right >= OBS_GAP:
            self.spawn_obstacle()

    def show_game_over(self):
        game_over_text = self.font.render('Game Over!', True, WHITE)
        self.screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
        pygame.display.flip()

    def handle_game_over(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += 0.5  # Gravity
        self.rect.y += int(self.velocity)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -10

    def reset(self):
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0

    def check_collision(self, obstacles):
        return pygame.sprite.spritecollide(self, obstacles, False)

    def check_boundaries(self):
        return self.rect.top <= 0 or self.rect.bottom >= HEIGHT


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, height, is_top):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((OBS_WIDTH, height))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        if is_top:
            self.rect.bottomleft = (x, 0)
        else:
            self.rect.topleft = (x, HEIGHT - height)

        self.velocity = OBS_SPEED
        self.game.all_sprites.add(self)
        self.game.obstacles.add(self)

    def update(self):
        self.rect.x += self.velocity
        if self.rect.right < 0:
            self.kill()

    @classmethod
    def create_pair(cls, game, x, gap_top, gap_bottom):
        top_height = gap_top
        bottom_height = HEIGHT - gap_bottom
        cls(game, x, top_height, True)
        cls(game, x, bottom_height, False)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
    pygame.quit()

