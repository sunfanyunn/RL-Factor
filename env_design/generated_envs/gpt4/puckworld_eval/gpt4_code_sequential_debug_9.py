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
        self.font = pygame.font.SysFont(None, 24)
        self.agent = Agent(self)
        self.green_dot = GreenDot()
        self.red_puck = RedPuck(self)
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.agent, self.green_dot, self.red_puck)
        self.score = 0

    def run(self):
        """Game loop given the pygame event"""
        self.screen.fill(BLACK)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)
            self.red_puck.update(self.agent.rect.center)

            self.sprites.update()
            self.check_collisions()

            self.screen.fill(BLACK)
            self.sprites.draw(self.screen)
            self.render_score()
            pygame.display.flip()

            self.clock.tick(FPS)

        return True

    def check_collisions(self):
        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()
        else:
            distance = pygame.math.Vector2(self.agent.rect.center) - pygame.math.Vector2(self.green_dot.rect.center)
            self.score -= RED_PENALTY_FACTOR * math.hypot(distance.x, distance.y)

        if pygame.sprite.collide_circle(self.agent, self.red_puck):
            self.score -= RED_PENALTY_FACTOR * 100

    def render_score(self):
        score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (10, 10))


class Agent(pygame.sprite.Sprite):

    def __init__(self, game):
        """Initialize the agent. Accept the game instance to access the screen and other components."""
        super().__init__()
        self.game = game
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.radius = 12
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
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
            thrust.scale_to_length(0.5)
            self.velocity += thrust
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        self.rect.clamp_ip(self.game.screen.get_rect())


class RedPuck(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.radius = radius
        self.speed = 1
        self.game = game

    def update(self, target):
        direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
            self.rect.move_ip(direction.x, direction.y)
        self.rect.clamp_ip(self.game.screen.get_rect())


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 5
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.radius = radius

    def randomize_position(self):
        self.rect.center = (random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius))

    def update(self):
        pass

if __name__ == "__main__":
    game = Game()
    running = game.run()
    pygame.quit()
    sys.exit()
