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
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self):
        """please implement the game loop here, given the pygame event"""
        self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.agent.update()
        self.red_puck.update(self.agent.rect.center)
        if self.green_dot.update(self.agent):
            self.green_dot.randomize_position()

        distance_to_green = math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx, self.agent.rect.centery - self.green_dot.rect.centery)
        self.score += GREEN_REWARD / distance_to_green if distance_to_green > 0 else GREEN_REWARD

        distance_to_red = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
        self.score -= RED_PENALTY_FACTOR / distance_to_red if distance_to_red > 0 else RED_PENALTY_FACTOR

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.display_score()

        pygame.display.flip()

        return True

    def display_score(self):
        score_surf = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_surf, (10, 10))


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
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
            thrust.scale_to_length(1)

        self.velocity += thrust
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)

class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.x = random.randint(0, WIDTH - 10)
        self.rect.y = random.randint(0, HEIGHT - 10)

    def update(self, agent):
        hit = pygame.sprite.collide_rect(self, agent)
        if hit:
            return True
        return False


if __name__ == '__main__':
    pygame.init()
    game = Game()
    running = True
    while running:
        running = game.run()
    pygame.quit()
    sys.exit()
