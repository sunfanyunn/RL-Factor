import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 5

# Enemy settings
ENEMY_SIZE = 30  # Reduced size of the aliens
ENEMY_SPEED = 2
ENEMY_ROWS = 4
ENEMY_COLS = 8


class SpaceInvadersGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.create_enemies()

    def create_enemies(self):
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                enemy = Enemy(col * (ENEMY_SIZE + 10), row * (ENEMY_SIZE + 10))
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                elif event.key == pygame.K_r and self.game_over:
                    # Restart the game when 'r' is pressed
                    self.restart_game()

    def update(self):
        self.all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)

        # Check if the enemies have reached the screen edge
        reached_edge = any(enemy.reached_edge() for enemy in self.enemies)
        if reached_edge:
            # Shift all enemies down only once per reaching the edge
            for e in self.enemies:
                e.move_down()

            # Change the direction of the entire group
            for e in self.enemies:
                e.change_direction()

        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.game_over = True

    def restart_game(self):
        # Reset game state for a new game
        self.game_over = False
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.create_enemies()

    def render_game(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        while True:  # Run the game loop indefinitely
            while not self.game_over:
                self.handle_events()
                self.update()
                self.render_game()

            # Display game over message
            self.screen.fill(BLACK)
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over. Press 'r' to restart.", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()

            # Event handling during game over screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - PLAYER_SIZE)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        game.all_sprites.add(bullet)
        game.bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # 1 for right, -1 for left
        self.reached_edge_flag = False  # To track if the enemy has reached the edge

    def update(self):
        self.rect.x += ENEMY_SPEED * self.direction
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1  # Reverse direction when reaching screen edge

    def move_down(self):
        if not self.reached_edge_flag:
            self.rect.y += (
                ENEMY_SIZE + 10
            )  # Move down by the height of an enemy + some space
            self.reached_edge_flag = True  # Set the flag to True after moving down

    def reached_edge(self):
        # Reset the flag when the enemy is not colliding with the edge
        if self.rect.left > 0 and self.rect.right < WIDTH:
            self.reached_edge_flag = False
        return self.rect.left <= 0 or self.rect.right >= WIDTH

    def change_direction(self):
        self.direction *= -1  # Reverse direction for the entire group


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()


if __name__ == "__main__":
    game = SpaceInvadersGame()
    game.run()
