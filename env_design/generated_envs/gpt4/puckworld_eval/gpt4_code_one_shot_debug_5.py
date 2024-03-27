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
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.score = 0

        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.all_sprites.add(self.green_dot)
        self.all_sprites.add(self.red_puck)

        self.green_dot.randomize_position()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BLACK)

            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)
            self.agent.update()
            self.red_puck.update(self.agent)
            self.green_dot.update()

            self.all_sprites.draw(self.screen)

            close_green = self.agent.get_distance(self.agent.rect.center, self.green_dot.rect.center) < 25
            if close_green:
                self.score += GREEN_REWARD
                self.green_dot.randomize_position()
            close_red = self.agent.get_distance(self.agent.rect.center, self.red_puck.rect.center) < 60
            if close_red:
                self.score -= RED_PENALTY_FACTOR

            self.display_score()
            pygame.display.flip()
            self.clock.tick(FPS)
        return running

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
        self.rect.clamp_ip(self.screen.get_rect())

    @staticmethod
    def get_distance(pos1, pos2):
        return math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])

class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randrange(0, WIDTH), random.randrange(0, HEIGHT)))
        self.speed = 1

    def update(self, target):
        target_center = target.rect.center
        direction = pygame.math.Vector2(target_center) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)

class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.center = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    pygame.quit()
    sys.exit()