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
        self.font = pygame.font.SysFont(None, 24)

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        distance = self.get_distance(self.agent.rect.center, self.green_dot.rect.center)
        self.score += max(0, int(GREEN_REWARD / (distance + 1)))
        distance_to_red_puck = self.get_distance(self.agent.rect.center, self.red_puck.rect.center)
        self.score -= int(RED_PENALTY_FACTOR * max(0, (150 - distance_to_red_puck)))

        self.red_puck.update(self.agent.rect.center)
        if event.type == pygame.QUIT:
            return False
        if distance < 25:  # Agent has reached the green dot
            self.green_dot.randomize_position()

        self.green_dot.update()
        self.agent.update()

        self.screen.fill(BLACK)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.screen.blit(self.green_dot.image, self.green_dot.rect)
        self.screen.blit(self.red_puck.image, self.red_puck.rect)

        score_text = self.font.render('Score: {}'.format(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    @staticmethod
    def get_distance(pos1, pos2):
        return math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the agent
        velocity: the agent's speed
        max_speed: the maximum speed of the agent
        """
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (10, 10), 10)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def apply_thrusters(self, keys):
        pass


    def update(self):
        pass


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
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))


    def update(self, target):
        pass


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
        self.rect.x = random.randint(0, WIDTH - 10)
        self.rect.y = random.randint(0, HEIGHT - 10)

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
