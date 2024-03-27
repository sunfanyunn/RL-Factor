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
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

        self.score = 0.0

    def get_distance(self, sprite1, sprite2):
        """Calculate the distance between two sprites."""
        return math.hypot(sprite1.rect.centerx - sprite2.rect.centerx, sprite1.rect.centery - sprite2.rect.centery)

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.red_puck.update(self.agent)
        self.all_sprites.update()

        # Scoring system
        distance_to_green_dot = self.get_distance(self.agent, self.green_dot)
        distance_to_red_puck = self.get_distance(self.agent, self.red_puck)
        self.score += GREEN_REWARD / distance_to_green_dot - distance_to_red_puck * RED_PENALTY_FACTOR

        # Check for collisions
        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()

        # Drawing
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        if event.type == pygame.QUIT:
            return False

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
        self.velocity = pygame.Vector2(0, 0)
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
        # Keep the agent within the screen boundaries
        self.rect.clamp_ip(self.screen.get_rect())


class RedPuck(pygame.sprite.Sprite):
    """Class representing the red puck obstacle"""

    def __init__(self):
        """Initialize the red puck
        speed: the speed of the red puck
        """
        super().__init__()
        radius = 30  # Increased size
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 2

    def update(self, target):
        """Update the red puck's position"""
        # Move the red puck towards the agent
        direction_vector = pygame.Vector2(target.rect.centerx - self.rect.centerx, target.rect.centery - self.rect.centery)
        if direction_vector.length() > 0:  # Avoid division by zero
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
        # The green dot does not move on its own, so no update logic is needed here
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
