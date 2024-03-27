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
        self.font = pygame.font.Font(None, 36)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def get_distance(self, entity1, entity2):
        """Return the distance between two entities."""
        return math.hypot(entity1.rect.centerx - entity2.rect.centerx, entity1.rect.centery - entity2.rect.centery)

    def run(self, event):
        """Implement the game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)
            self.red_puck.update(self.agent)
            self.green_dot.update()

            score_change = 0
            agent_green_distance = self.get_distance(self.agent, self.green_dot)
            score_change += max(GREEN_REWARD - agent_green_distance, 0)

            agent_red_distance = self.get_distance(self.agent, self.red_puck)
            score_change -= min(agent_red_distance, GREEN_REWARD) * RED_PENALTY_FACTOR

            self.score += score_change
            score_text = self.font.render(f"Score: {int(self.score)}", True, WHITE)
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(FPS)

        return True


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        thrust = pygame.Vector2(0, 0)
        if keys[pygame.K_UP]:
            thrust.y = -1
        if keys[pygame.K_DOWN]:
            thrust.y = 1
        if keys[pygame.K_LEFT]:
            thrust.x = -1
        if keys[pygame.K_RIGHT]:
            thrust.x = 1

        thrust = thrust.normalize_or_zero() * self.max_speed
        self.velocity += thrust
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity.x = -self.velocity.x
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity.y = -self.velocity.y

        self.rect.clamp_ip(self.screen.get_rect())


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 1

    def update(self, target):
        movement = pygame.Vector2(target.rect.centerx - self.rect.centerx, 
                                  target.rect.centery - self.rect.centery)
        if movement.length() > 0:
            movement.scale_to_length(self.speed)
        self.rect.move_ip(movement)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def update(self):
        if self.rect.colliderect(self.agent.rect):
            self.randomize_position()


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
