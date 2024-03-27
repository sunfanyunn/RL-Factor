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

        self.agent_group = pygame.sprite.Group(self.agent)
        self.green_dot_group = pygame.sprite.Group(self.green_dot)
        self.red_puck_group = pygame.sprite.Group(self.red_puck)

        self.score = 0

        self.green_dot.randomize_position()

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        # Scoring
        distance_to_green = math.hypot(
            self.agent.rect.centerx - self.green_dot.rect.centerx,
            self.agent.rect.centery - self.green_dot.rect.centery
        )
        self.score += int(GREEN_REWARD / distance_to_green) if distance_to_green else GREEN_REWARD

        # Check collision with green dot
        if pygame.sprite.spritecollide(self.agent, self.green_dot_group, True):
            self.green_dot = GreenDot()
            self.green_dot_group.add(self.green_dot)
            self.green_dot.randomize_position()

        distance_to_red = math.hypot(
            self.agent.rect.centerx - self.red_puck.rect.centerx,
            self.agent.rect.centery - self.red_puck.rect.centery
        )
        self.score -= int(RED_PENALTY_FACTOR * distance_to_red)

        # Draw everything
        self.screen.fill(BLACK)
        self.agent_group.draw(self.screen)
        self.green_dot_group.draw(self.screen)
        self.red_puck_group.draw(self.screen)

        score_text = self.font.render('Score: {}'.format(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize the agent"
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        if keys[pygame.K_LEFT]:
            self.velocity.x = max(self.velocity.x - 1, -self.max_speed)
        if keys[pygame.K_RIGHT]:
            self.velocity.x = min(self.velocity.x + 1, self.max_speed)
        if keys[pygame.K_UP]:
            self.velocity.y = max(self.velocity.y - 1, -self.max_speed)
        if keys[pygame.K_DOWN]:
            self.velocity.y = min(self.velocity.y + 1, self.max_speed)

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
    """Class representing the red puck obstacle"

    def __init__(self):
        super().__init__()
        radius = 30  # Half the diameter to make radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        self.speed = 1

    def update(self, target):
        target_vector = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if target_vector.length() > 0:
            target_vector = target_vector.normalize() * self.speed
        self.rect.move_ip(target_vector)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
    pygame.quit()
    sys.exit()
