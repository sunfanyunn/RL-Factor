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
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
        self.score = 0

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.red_puck.update(self.agent.rect.center)

        agent_distance = math.hypot((self.agent.rect.x - self.green_dot.rect.x), (self.agent.rect.y - self.green_dot.rect.y))
        puck_distance = math.hypot((self.agent.rect.x - self.red_puck.rect.x), (self.agent.rect.y - self.red_puck.rect.y))

        self.score += GREEN_REWARD / agent_distance - RED_PENALTY_FACTOR / puck_distance

        if self.agent.rect.colliderect(self.green_dot.rect):
            self.green_dot.randomize_position()

        self.green_dot.update()

        self.screen.fill(BLACK)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.screen.blit(self.green_dot.image, self.green_dot.rect)
        self.screen.blit(self.red_puck.image, self.red_puck.rect)

        score_text = pygame.font.SysFont(None, 36).render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (5, 5))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the agent
        velocity: the agent's speed
        max_speed: the maximum speed of the agent
        """
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        """Apply thrust based on user input"""
        if keys[pygame.K_LEFT]:
            self.velocity.x = max(self.velocity.x - 1, -self.max_speed)
        if keys[pygame.K_RIGHT]:
            self.velocity.x = min(self.velocity.x + 1, self.max_speed)
        if keys[pygame.K_UP]:
            self.velocity.y = max(self.velocity.y - 1, -self.max_speed)
        if keys[pygame.K_DOWN]:
            self.velocity.y = min(self.velocity.y + 1, self.max_speed)

    def update(self):
        """Update the agent's position"""
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity.x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity.y = 0


class RedPuck(pygame.sprite.Sprite):
    """Class representing the red puck obstacle"""

    def __init__(self):
        """Initialize the red puck
        speed: the speed of the red puck
        """
        super().__init__()
        radius = 60  # Increased size
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        """Update the red puck's position"""
        target_vector = pygame.math.Vector2(target)
        puck_vector = pygame.math.Vector2(self.rect.center)
        direction_vector = (target_vector - puck_vector).normalize()
        self.rect.center += direction_vector * self.speed


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the green dot
        """
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        """Randomize the green dot's position"""
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

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
