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
        self.font = pygame.font.Font(None, 36)
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.agent)
        self.sprites.add(self.green_dot)
        self.sprites.add(self.red_puck)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)

        self.check_collisions()

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (5, 10))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def check_collisions(self):
        if self.agent.rect.colliderect(self.green_dot.rect):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()

        if self.agent.rect.colliderect(self.red_puck.rect):
            distance_to_red = pygame.Vector2(self.agent.rect.center) - pygame.Vector2(self.red_puck.rect.center)
            penalty = math.ceil(distance_to_red.length_squared() / (RED_PENALTY_FACTOR * RED_PENALTY_FACTOR))
            self.score -= penalty
        self.score = max(self.score, 0)


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        accel = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            accel.x -= 1
        if keys[pygame.K_RIGHT]:
            accel.x += 1
        if keys[pygame.K_UP]:
            accel.y -= 1
        if keys[pygame.K_DOWN]:
            accel.y += 1
        if accel.length_squared() != 0:  # Avoid dividing by zero
            accel.normalize_ip()
        accel *= 0.5
        self.velocity += accel
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 2

    def update(self, target):
        direction = pygame.Vector2(target) - pygame.Vector2(self.rect.center)
        if direction.length_squared() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.center = (random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5))

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
    sys.exit()
