import pygame
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_WIDTH = 70
OBSTACLE_GAP_SIZE = 200
OBSTACLE_SPEED = 5
SCORE_PER_PASS = 1


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
        self.font = pygame.font.Font(None, 36)

        self.spawn_obstacle()

    def spawn_obstacle(self):
        position = self.generate_obstacle_positions()
        obstacle = Obstacle(*position)
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def reset_game(self):
        self.player.reset()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.score = 0
        self.game_over = False
        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif not self.game_over and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            self.player.jump()

        if not self.game_over:
            self.all_sprites.update()
            self.handle_collisions()
            self.increment_score()
            self.spawn_obstacle_if_needed()

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.show_score()
            pygame.display.flip()
            self.clock.tick(FPS)
        else:
            self.handle_game_over(event)

        return True

    def handle_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.obstacles, False) or not self.player.rect.inflate(0, -10).colliderect(self.screen.get_rect()):
            self.game_over = True

    def generate_obstacle_positions(self):
        last_obstacle = max(self.obstacles, key=lambda ob: ob.rect.right, default=None)
        spacing = WIDTH // 2 if last_obstacle is None else max(WIDTH // 2 - last_obstacle.rect.right, 0)
        hole_top = random.randint(100, HEIGHT - OBSTACLE_GAP_SIZE - 100)
        hole_bottom = hole_top + OBSTACLE_GAP_SIZE
        return hole_top, hole_bottom, spacing

    def show_score(self):
        score_surf = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_surf, (10, 10))

    def handle_game_over(self, event):
        game_over_surf = self.font.render('Game Over!', True, WHITE)
        self.screen.blit(game_over_surf, (WIDTH // 2 - game_over_surf.get_width() // 2, HEIGHT // 2 - game_over_surf.get_height() // 2))
        pygame.display.flip()

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.reset_game()

    def increment_score(self):
        for obstacle in self.obstacles:
            if obstacle.rect.right < self.player.rect.left and not obstacle.score_counted:
                self.score += SCORE_PER_PASS
                obstacle.score_counted = True

    def spawn_obstacle_if_needed(self):
        if len(self.obstacles) < 2:
            self.spawn_obstacle()


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
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def reset(self):
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top, bottom, spacing):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, HEIGHT), pygame.SRCALPHA)
        top_section_height = top
        bottom_section_height = HEIGHT - bottom
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, WHITE, pygame.Rect(0, 0, OBSTACLE_WIDTH, top_section_height))
        pygame.draw.rect(self.image, WHITE, pygame.Rect(0, bottom, OBSTACLE_WIDTH, bottom_section_height))
        self.rect = self.image.get_rect(right=WIDTH + spacing)

        self.score_counted = False

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


