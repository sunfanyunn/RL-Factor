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
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.score = 0
        self.clock = pygame.time.Clock()

    def run(self, event):
        self.screen.fill(BLACK)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        closeness = max(0, GREEN_REWARD - int(math.hypot(
            self.agent.rect.centerx - self.green_dot.rect.centerx,
            self.agent.rect.centery - self.green_dot.rect.centery)))
        self.score += closeness
        distance_to_puck = math.hypot(
            self.agent.rect.centerx - self.red_puck.rect.centerx,
            self.agent.rect.centery - self.red_puck.rect.centery)
        if distance_to_puck < self.red_puck.radius:
            self.score -= RED_PENALTY_FACTOR

        if self.agent.rect.colliderect(self.green_dot.rect):
            self.green_dot.randomize_position()

        score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(self.agent.image, self.agent.rect)
        self.screen.blit(self.green_dot.image, self.green_dot.rect)
        self.screen.blit(self.red_puck.image, self.red_puck.rect)

        pygame.display.flip()
        self.clock.tick(FPS)

        return True


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = [0, 0]
        self.max_speed = 5

    def apply_thrusters(self, keys):
        thrust = 0.1
        if keys[pygame.K_UP]:
            self.velocity[1] -= thrust
        if keys[pygame.K_DOWN]:
            self.velocity[1] += thrust
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= thrust
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += thrust

        # Clamp the velocity to the maximum speed
        speed = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity[0] *= scale
            self.velocity[1] *= scale

    def update(self):
        self.rect.x += int(self.velocity[0])
        self.rect.y += int(self.velocity[1])

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # Damping
        self.velocity[0] *= 0.9
        self.velocity[1] *= 0.9


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 60
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)))
        self.speed = 1

    def update(self, target):
        direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        new_pos = pygame.math.Vector2(self.rect.center) + direction
        self.rect.center = (int(new_pos.x), int(new_pos.y))


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.topleft = (random.randint(0, WIDTH - self.rect.width), random.randint(0, HEIGHT - self.rect.height))

    def update(self):
        pass


if __name__ == "__main__":
    pygame.font.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
    pygame.quit()
    sys.exit()
