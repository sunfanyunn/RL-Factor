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
        self.sprites = pygame.sprite.Group(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.calculate_score()
        self.red_puck.update(self.agent)
        self.green_dot.update()

        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        if event.type == pygame.QUIT:
            return False

        return True

    def calculate_score(self):
        if self.agent.rect.colliderect(self.green_dot.rect):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()
        green_x, green_y = self.green_dot.rect.center
        red_x, red_y = self.red_puck.rect.center
        agent_x, agent_y = self.agent.rect.center
        distance_to_green = math.hypot(green_x - agent_x, green_y - agent_y)
        distance_to_red = math.hypot(red_x - agent_x, red_y - agent_y)
        penalty = max(0, RED_PENALTY_FACTOR * (self.red_puck.radius - distance_to_red))
        self.score -= penalty
        self.score = max(self.score, 0)  # Prevent negative score

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
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            thrust.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            thrust.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            thrust.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            thrust.y = 1
        self.velocity += thrust
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity.x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity.y = 0

class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 60  # Increased size
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)))
        self.speed = 1

    def update(self, target):
        target_vector = pygame.math.Vector2(target.rect.center) - pygame.math.Vector2(self.rect.center)
        if target_vector.length() > 0:
            target_vector.scale_to_length(self.speed)
        self.rect.move_ip(target_vector)

class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def update(self):
        pass

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
