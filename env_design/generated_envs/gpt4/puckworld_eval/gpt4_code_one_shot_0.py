
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
        self.red_puck = RedPuck()
        self.green_dot.randomize_position()
        self.score = 0

    def run(self, event):
        """Implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.red_puck.update(self.agent.rect.center)
        self.green_dot.update()
        distance_to_green = math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx,
                                       self.agent.rect.centery - self.green_dot.rect.centery)
        distance_to_red = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx,
                                     self.agent.rect.centery - self.red_puck.rect.centery)
        if distance_to_green < 15:
            self.green_dot.randomize_position()
            self.score += GREEN_REWARD
        self.score -= distance_to_red / RED_PENALTY_FACTOR

        self.screen.fill(BLACK)
        self.green_dot.draw(self.screen)
        self.red_puck.draw(self.screen)
        self.agent.draw(self.screen)

        score_text = pygame.font.Font(None, 36).render('Score: ' + str(int(self.score)), True, WHITE)
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
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        """Apply thrust based on user input"""
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
            thrust.scale_to_length(1)
            self.velocity += thrust
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

    def update(self):
        """Update the agent's position"""
        self.rect.move_ip(self.velocity.x, self.velocity.y)
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
    """Class representing the red puck obstacle"""

    def __init__(self):
        """Initialize the red puck
        speed: the speed of the red puck
        """
        super().__init__()
        radius = 60  # Increased size
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 1  # Slow and menacing

    def update(self, target):
        """Update the red puck's position"""
        direction = (pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.centerx, self.rect.centery)).normalize()
        self.rect.move_ip(direction.x * self.speed, direction.y * self.speed)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the green dot
        """
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        """Randomize the green dot's position"""
        x = random.randint(0, WIDTH - 10)
        y = random.randint(0, HEIGHT - 10)
        self.rect.topleft = (x, y)

    def update(self):
        """Ensure the green dot's randomized position is fixed during the update"""
        pass  # No need to update position unless it's being collided with

    def draw(self, surface):
        """Draw the green dot on the surface"""
        surface.blit(self.image, self.rect)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
