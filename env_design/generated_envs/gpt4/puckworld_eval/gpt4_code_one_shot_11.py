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
        self.font = pygame.font.SysFont(None, 24)

        self.agent = Agent()
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
    
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        self.score += self.calculate_score()

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.display_score()

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

    def calculate_score(self):
        agent_green_distance = self.distance(self.agent.rect.center, self.green_dot.rect.center)
        score_increase = max(0, GREEN_REWARD - agent_green_distance)

        agent_red_distance = self.distance(self.agent.rect.center, self.red_puck.rect.center)
        score_decrease = max(0, RED_PENALTY_FACTOR * (agent_red_distance - self.red_puck.radius))

        return score_increase - score_decrease

    def display_score(self):
        score_surf = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_surf, (10, 10))

    @staticmethod
    def distance(point1, point2):
        return math.hypot(point1[0] - point2[0], point1[1] - point2[1])


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 12
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

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
        self.rect.center += self.velocity
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        elif self.rect.top > HEIGHT:
            self.rect.bottom = 0


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 30
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 4))

        self.speed = 1

    def update(self, target):
        direction = pygame.math.Vector2(target) - self.rect.center
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.center += direction


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
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
        running = game.run(event)
    pygame.quit()
    sys.exit()
