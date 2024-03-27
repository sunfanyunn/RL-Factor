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
        self.spawn_obstacle()

    def spawn_obstacle(self):
        top_gap = random.randint(50, HEIGHT - CAVERN_WIDTH - 50)
        bottom_gap = top_gap + CAVERN_WIDTH
        obstacle_top = Obstacle(bottom=top_gap)
        obstacle_bottom = Obstacle(top=bottom_gap)
        self.obstacles.add(obstacle_top, obstacle_bottom)
        self.all_sprites.add(obstacle_top, obstacle_bottom)

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.player.reset()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.spawn_obstacle()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            self.player.jump()
        self.screen.fill(BLACK)
        if not self.game_over:
            self.player.update()
            self.obstacles.update()

            for obstacle in list(self.obstacles):
                if obstacle.rect.right < 0:
                    self.obstacles.remove(obstacle)
                    self.all_sprites.remove(obstacle)
                    self.score += 0.5
                    self.spawn_obstacle()

            self.all_sprites.draw(self.screen)

            if pygame.sprite.spritecollide(self.player, self.obstacles, False) or self.player.rect.top < 0 or self.player.rect.bottom > HEIGHT:
                self.game_over = True

            self.display_score()
        else:
            self.display_message("Game Over! Press SPACE to restart", WHITE)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset_game()

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

    def display_message(self, text, color):
        font = pygame.font.SysFont(None, 48)
        message = font.render(text, True, color)
        message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message, message_rect)

    def display_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render('Score: ' + str(int(self.score)), True, WHITE)
        self.screen.blit(score_text, (10, 10))


class Pixelcopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0
        self.gravity = 0.5
        self.jump_speed = -10

    def update(self):
        self.velocity += self.gravity
        self.rect.y += int(self.velocity)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = self.jump_speed

    def reset(self):
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.velocity = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, top=None, bottom=None):
        super().__init__()
        self.image = pygame.Surface((30, HEIGHT))
        if top is not None and bottom is None:
            self.image = pygame.transform.scale(self.image, (30, top))
        elif bottom is not None and top is None:
            self.image = pygame.transform.scale(self.image, (30, HEIGHT - bottom))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(x=WIDTH)
        if top is not None:
            self.rect.bottom = top
        if bottom is not None:
            self.rect.top = bottom

    def update(self):
        self.rect.x -= 2


if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game.game_over or (game.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                running = game.run(event)
    pygame.quit()
