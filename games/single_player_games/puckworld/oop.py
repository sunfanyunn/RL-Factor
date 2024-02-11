import pygame
import sys
import random
import math

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class PuckWorld:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group(
            self.agent, self.green_dot, self.red_puck
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

    def update_game(self):
        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent)

        if self.agent.rect.colliderect(self.green_dot.rect):
            self.green_dot.randomize_position()

        if self.agent.rect.colliderect(self.red_puck.rect):
            self.game_over = True

    def render_game(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.update_game()
            self.render_game()


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH // 2, HEIGHT // 2)
        self.velocity = [0, 0]
        self.thruster_force = 1
        self.velocity_decay = 0.98

    def apply_thrusters(self, keys):
        if keys[pygame.K_UP]:
            self.velocity[1] -= self.thruster_force
        if keys[pygame.K_DOWN]:
            self.velocity[1] += self.thruster_force
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= self.thruster_force
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += self.thruster_force

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

        self.velocity[0] *= self.velocity_decay
        self.velocity[1] *= self.velocity_decay


class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.topleft = (
            random.randint(0, WIDTH - self.rect.width),
            random.randint(0, HEIGHT - self.rect.height),
        )

    def update(self):
        pass


class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Increase the radius value to make the red puck bigger
        radius = 40
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = (WIDTH // 4, HEIGHT // 4)
        self.speed = 1

    def update(self, target):
        angle = math.atan2(
            target.rect.centery - self.rect.centery,
            target.rect.centerx - self.rect.centerx,
        )
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))


if __name__ == "__main__":
    game = PuckWorld()
    game.run()
