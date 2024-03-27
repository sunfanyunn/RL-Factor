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
        self.font = pygame.font.Font(None, 36)
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

    def run(self, event):
        self.screen.fill(BLACK)
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.green_dot.update(self.agent.get_distance(self.green_dot.rect.center))
        self.red_puck.update(self.agent.rect.center)

        if self.agent.rect.colliderect(self.green_dot.rect):
            self.agent.score += GREEN_REWARD
            self.green_dot.randomize_position()

        green_distance = self.agent.get_distance(self.green_dot.rect.center)
        red_distance = self.agent.get_distance(self.red_puck.rect.center)

        if green_distance > 0:
            self.agent.score += GREEN_REWARD / green_distance
        if red_distance > 0:
            self.agent.score -= RED_PENALTY_FACTOR / red_distance

        for entity in [self.agent, self.green_dot, self.red_puck]:
            self.screen.blit(entity.image, entity.rect)

        score_text = self.font.render(f'Score: {int(self.agent.score)}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        return True


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5
        self.score = 0

    def apply_thrusters(self, keys):
        thrust = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            thrust.x = -1
        if keys[pygame.K_RIGHT]:
            thrust.x = 1
        if keys[pygame.K_UP]:
            thrust.y = -1
        if keys[pygame.K_DOWN]:
            thrust.y = 1

        if thrust.length() > 0:
            thrust.normalize_ip()
            thrust.scale_to_length(self.max_speed)
        self.velocity = 0.9 * self.velocity + 0.1 * thrust

    def update(self):
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def get_distance(self, target_pos):
        target_vector = pygame.math.Vector2(target_pos)
        dist = target_vector.distance_to(pygame.math.Vector2(self.rect.center))
        return dist


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 2

    def update(self, target):
        target_vector = pygame.math.Vector2(target)
        direction = target_vector - pygame.math.Vector2(self.rect.center)
        if direction.length_squared() > 0:
            direction.normalize_ip()
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect(center=(random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5)))

    def randomize_position(self):
        self.rect.center = (random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5))

    def update(self, distance):
        if random.randint(0,100) < 2:  # Approx. 2% chance to move each frame
            direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            direction.normalize_ip()
            self.rect.move_ip(direction * 5)
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # Keep inside screen bounds

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
