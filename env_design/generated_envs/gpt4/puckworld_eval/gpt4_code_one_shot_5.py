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
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.all_sprites.add(self.green_dot)
        self.all_sprites.add(self.red_puck)
        self.green_dot.randomize_position()
        self.score = 0

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.red_puck.update(self.agent)
        self.all_sprites.update()

        close_green = self.get_distance(self.agent.rect.center, self.green_dot.rect.center) < 25
        if close_green:
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()
        close_red = self.get_distance(self.agent.rect.center, self.red_puck.rect.center) < 60
        if close_red:
            self.score -= RED_PENALTY_FACTOR

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.display_score()
        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def get_distance(self, pos1, pos2):
        return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

    def display_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
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
        self.velocity += thrust
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity)


class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 1

    def update(self, target):
        target_center = target.rect.center
        direction = (target_center[0] - self.rect.centerx, target_center[1] - self.rect.centery)
        distance = math.sqrt(direction[0]**2 + direction[1]**2)
        if distance > 0:
            direction = (direction[0]/distance, direction[1]/distance)
            self.rect.centerx += direction[0] * self.speed
            self.rect.centery += direction[1] * self.speed


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.center = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))

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

