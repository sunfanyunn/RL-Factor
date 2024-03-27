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
        self.font = pygame.font.SysFont(None, 36)

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False
        self.agent.apply_thrusters(pygame.key.get_pressed())
        self.agent.update()
        self.red_puck.update(self.agent.rect.center)
        self.green_dot.update()
        agent_distance_to_green = math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx, self.agent.rect.centery - self.green_dot.rect.centery)
        agent_distance_to_red = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
        self.score += (GREEN_REWARD / agent_distance_to_green) - (RED_PENALTY_FACTOR / agent_distance_to_red)
        if self.agent.rect.colliderect(self.green_dot.rect):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()
        self.screen.fill(BLACK)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.screen.blit(self.green_dot.image, self.green_dot.rect)
        self.screen.blit(self.red_puck.image, self.red_puck.rect)
        score_surf = self.font.render('Score: %d' % self.score, True, WHITE)
        self.screen.blit(score_surf, (10, 10))
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
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        """Apply thrust based on user input"""
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
        """Update the agent's position"""
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT


class RedPuck(pygame.sprite.Sprite):
    """Class representing the red puck obstacle"""

    def __init__(self):
        """Initialize the red puck
        speed: the speed of the red puck
        """
        super().__init__()
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.speed = 2

    def update(self, target):
        """Update the red puck's position"""
        direction_vector = pygame.math.Vector2(target) - self.rect.center
        if direction_vector.length() > 0:
            direction_vector.scale_to_length(self.speed)
            self.rect.move_ip(direction_vector)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the green dot
        """
        super().__init__()
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()

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
