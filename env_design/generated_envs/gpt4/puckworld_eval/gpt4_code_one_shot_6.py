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

    def run(self, event):
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        self.agent.update()

        closeness = max(0, GREEN_REWARD - int(math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx, self.agent.rect.centery - self.green_dot.rect.centery)))
        self.score += closeness
        distance_to_puck = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
        if distance_to_puck < self.red_puck.radius:
            self.score -= RED_PENALTY_FACTOR

        self.screen.fill(BLACK)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.screen.blit(self.green_dot.image, self.green_dot.rect)
        self.screen.blit(self.red_puck.image, self.red_puck.rect)

        if self.agent.rect.colliderect(self.green_dot.rect):
            self.green_dot.randomize_position()
        score_text = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
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
        if keys[pygame.K_UP]:
            self.velocity[1] -= 0.5
        if keys[pygame.K_DOWN]:
            self.velocity[1] += 0.5
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= 0.5
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += 0.5

        speed = math.hypot(*self.velocity)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity[0] *= scale
            self.velocity[1] *= scale

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity[0] = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity[0] = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity[1] = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity[1] = 0


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 60
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 1

    def update(self, target):
        direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        self.rect.centerx += int(direction.x)
        self.rect.centery += int(direction.y)


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
        running = game.run(event)
    pygame.quit()
    sys.exit()
