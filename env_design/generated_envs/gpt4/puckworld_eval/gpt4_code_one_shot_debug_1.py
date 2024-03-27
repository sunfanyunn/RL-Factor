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
        """Initialize the game
        agent: the player's character
        green_dot: the target for the agent
        red_puck: the obstacle for the agent
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.score = 0
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        """Implement the game loop."""
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.sprites.update()

        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()

        distance_to_red = self.agent.get_distance_to(self.red_puck.rect.center)
        if distance_to_red < self.red_puck.radius:
            self.score -= (self.red_puck.radius - int(distance_to_red)) * RED_PENALTY_FACTOR

        score_text = self.font.render('Score: ' + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the agent"""
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.radius = 12
        self.velocity = [0, 0]
        self.max_speed = 5

    def apply_thrusters(self, keys):
        """Apply thrust based on user input"""
        if keys[pygame.K_UP]:
            self.velocity[1] -= 1
        if keys[pygame.K_DOWN]:
            self.velocity[1] += 1
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= 1
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += 1

        self.velocity[0] = max(min(self.velocity[0], self.max_speed), -self.max_speed)
        self.velocity[1] = max(min(self.velocity[1], self.max_speed), -self.max_speed)

    def update(self):
        """Update the agent's position"""
        self.rect.move_ip(*self.velocity)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def get_distance_to(self, target):
        target_x, target_y = target
        return math.hypot(self.rect.centerx - target_x, self.rect.centery - target_y)


class RedPuck(pygame.sprite.Sprite):
    """Class representing the red puck obstacle"""

    def __init__(self):
        """Initialize the red puck"""
        super().__init__()
        self.radius = 60
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)))

    def update(self):
        """Update the red puck's position"""
        direction = [self.target[0] - self.rect.centerx, self.target[1] - self.rect.centery]
        length = math.hypot(*direction)
        if length > 0:
            direction[0] /= length
            direction[1] /= length

        self.rect.move_ip(direction[0] * 0.3, direction[1] * 0.3)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the green dot"""
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (7, 7), 5)
        self.rect = self.image.get_rect(center=(random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)))

    def randomize_position(self):
        """Randomize the green dot's position"""
        self.rect.center = (random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius))

    def update(self):
        """Update the green dot's position"""
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
