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
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.agent)
        self.sprites.add(self.green_dot)
        self.sprites.add(self.red_puck)

    def calculate_score(self):
        # Calculate distance between agent and green dot
        distance_to_green = self.agent.rect.centerx, self.agent.rect.centery
        distance_to_red = self.agent.rect.centerx, self.agent.rect.centery
        reward = max(GREEN_REWARD - math.hypot(green_x - agent_x, green_y - agent_y), 0)
        penalty = max(0, math.hypot(red_x - agent_x, red_y - agent_y) - self.red_puck.radius)
        self.score += reward - (RED_PENALTY_FACTOR * penalty)

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.sprites.update()
        self.calculate_score()
        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
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
        self.image = self.image.convert()
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        """Apply thrust based on user input"""
        thrust = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            thrust.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            thrust.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            thrust.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            thrust.y = 1
        self.velocity += thrust
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

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
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 1

    def update(self, target):
        """Update the red puck's position"""
        target_vector = pygame.math.Vector2(target.rect.center) - pygame.math.Vector2(self.rect.center)
        if target_vector.length() > 0:
            target_vector.scale_to_length(self.speed)
        self.rect.move_ip(target_vector)


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
