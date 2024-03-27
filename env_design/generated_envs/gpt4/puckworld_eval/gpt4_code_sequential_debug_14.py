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

GREEN_REWARD = 100
RED_PENALTY_FACTOR = 2


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.score_font = pygame.font.SysFont(None, 36)
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck(self.agent)
        self.all_sprites = pygame.sprite.Group(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.all_sprites.update()

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()
            self.score += GREEN_REWARD

        green_distance = self.agent.distance_to(self.green_dot.rect.center)
        red_distance = self.agent.distance_to(self.red_puck.rect.center)
        self.score += max(0, GREEN_REWARD // max(green_distance, 1) - RED_PENALTY_FACTOR * RED_PENALTY_FACTOR // max(red_distance, 1))

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_text = self.score_font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        acceleration = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            acceleration.x = -1
        if keys[pygame.K_RIGHT]:
            acceleration.x = 1
        if keys[pygame.K_UP]:
            acceleration.y = -1
        if keys[pygame.K_DOWN]:
            acceleration.y = 1
        acceleration *= 0.1
        self.velocity += acceleration
        if self.velocity.length() > 0:
            self.velocity *= min(self.max_speed / self.velocity.length(), 1)
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def distance_to(self, target):
        return math.hypot(self.rect.centerx - target[0], self.rect.centery - target[1])

    def update(self):
        pass

class RedPuck(pygame.sprite.Sprite):

    def __init__(self, agent):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 0.5
        self.agent = agent

    def update(self):
        target = self.agent.rect.center
        direction = pygame.math.Vector2(target[0] - self.rect.centerx, target[1] - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        self.rect.move_ip(direction)

class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect(center=self.random_position())

    def random_position(self):
        return random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20)

    def randomize_position(self):
        self.rect.center = self.random_position()

    def update(self):
        pass

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.NOEVENT:
            continue
        running = game.run(event)
    pygame.quit()
    sys.exit()
