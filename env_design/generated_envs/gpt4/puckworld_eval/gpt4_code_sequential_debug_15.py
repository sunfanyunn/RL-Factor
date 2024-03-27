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
        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.green_dot.randomize_position()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        running = True
        if event and event.type == pygame.QUIT:
            running = False
        else:
            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)

            self.green_dot.update()
            self.sprites.update()

            green_dist = math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx, self.agent.rect.centery - self.green_dot.rect.centery)
            if green_dist > 0:
                self.score += GREEN_REWARD / max(green_dist, 1)

            red_dist = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
            if red_dist > 0:
                self.score -= RED_PENALTY_FACTOR / max(red_dist, 1)

            if self.agent.rect.colliderect(self.green_dot.rect):
                self.score += GREEN_REWARD
                self.green_dot.randomize_position()

            self.screen.fill(BLACK)
            self.sprites.draw(self.screen)

            score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(FPS)

        return running


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2()
        self.max_speed = 5

    def apply_thrusters(self, keys):
        acceleration = 0.2
        if keys[pygame.K_LEFT]:
            self.velocity.x -= acceleration
        if keys[pygame.K_RIGHT]:
            self.velocity.x += acceleration
        if keys[pygame.K_UP]:
            self.velocity.y -= acceleration
        if keys[pygame.K_DOWN]:
            self.velocity.y += acceleration

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius = 15
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(WIDTH // 3, HEIGHT // 3))
        self.speed = 2

    def update(self):
        target = self.agent.rect.center
        direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if direction.length_squared() > 0:  # use length_squared() to avoid calculating the square root
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 5
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (radius, radius), radius)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.center = (random.uniform(self.radius, WIDTH - self.radius), random.uniform(self.radius, HEIGHT - self.radius))

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        running = game.run(None)
    pygame.quit()
    sys.exit()
