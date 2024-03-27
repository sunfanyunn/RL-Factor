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
RED_PENALTY_FACTOR = 0.02


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.score = 0
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.all_sprites = pygame.sprite.Group(self.agent, self.green_dot, self.red_puck)
        self.green_dot.randomize_position()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.red_puck.update(self.agent.rect.center)

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()

        distance_to_red = math.hypot(
            self.agent.rect.centerx - self.red_puck.rect.centerx,
            self.agent.rect.centery - self.red_puck.rect.centery
        )
        distance_penalty = int(distance_to_red * RED_PENALTY_FACTOR)
        self.score -= distance_penalty
        self.score = max(self.score, 0)

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.display_score()
        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_surface, (10, 10))


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        thrust = pygame.math.Vector2(0, 0)
        if keys[pygame.K_RIGHT]:
            thrust.x = 1
        if keys[pygame.K_LEFT]:
            thrust.x = -1
        if keys[pygame.K_DOWN]:
            thrust.y = 1
        if keys[pygame.K_UP]:
            thrust.y = -1
        thrust *= self.max_speed
        self.velocity += thrust
        if self.velocity.magnitude() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def update(self):
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 15
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 2

    def update(self, target):
        target_vector = pygame.math.Vector2(target)
        puck_vector = pygame.math.Vector2(self.rect.center)
        direction = target_vector - puck_vector
        if direction.magnitude() > 0:
            direction = direction.normalize() * self.speed
        self.rect.move_ip(direction)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 5
        self.image = pygame.Surface((2 * radius, 2 * radius))
        pygame.draw.circle(self.image, GREEN, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        radius = 5
        self.rect.center = (random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius))

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()