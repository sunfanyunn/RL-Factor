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
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.all_sprites.add(self.green_dot)
        self.all_sprites.add(self.red_puck)

        self.green_dot.randomize_position()

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.red_puck.update(self.agent.rect.center)

        self.score += self.calculate_score()

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_score()
        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def calculate_score(self):
        distance_to_green = math.hypot(*(Vector2(self.agent.rect.center) - Vector2(self.green_dot.rect.center)))
        distance_to_red = math.hypot(*(Vector2(self.agent.rect.center) - Vector2(self.red_puck.rect.center)))
        return -RED_PENALTY_FACTOR * (1 / (distance_to_red + 1e-5))

    def draw_score(self):
        score_surf = self.font.render('Score: {}'.format(self.score), True, WHITE)
        self.screen.blit(score_surf, (10, 10))


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the agent
        velocity: the agent's speed
        max_speed: the maximum speed of the agent
        """
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.velocity = Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        """Apply thrust based on user input"""
        acceleration = Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            acceleration.x = -1
        if keys[pygame.K_RIGHT]:
            acceleration.x = 1
        if keys[pygame.K_UP]:
            acceleration.y = -1
        if keys[pygame.K_DOWN]:
            acceleration.y = 1

        acceleration = acceleration.normalize_or_zero() * 0.5
        self.velocity += acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        """Update the agent's position"""
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


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
        self.rect = self.image.get_rect(center=(WIDTH//4, HEIGHT//4))
        self.speed = 2
    def update(self, target):
        """Update the red puck's position"""
        target_vector = Vector2(target) - Vector2(self.rect.center)
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
    def randomize_position(self):
        """Randomize the green dot's position"""
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)

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
