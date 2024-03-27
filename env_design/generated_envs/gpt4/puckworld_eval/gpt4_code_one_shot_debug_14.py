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
        self.font = pygame.font.Font(None, 36)
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.green_dot.randomize_position()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)
        self.score = 0

    def run(self, event):
        self.clock.tick(FPS)
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.red_puck.update(self.agent.rect.center)

        agent_green_distance = self.get_distance(self.agent.rect.center, self.green_dot.rect.center)
        if agent_green_distance < 25:
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()

        agent_red_distance = self.get_distance(self.agent.rect.center, self.red_puck.rect.center)
        if agent_red_distance < 25:
            self.score -= RED_PENALTY_FACTOR
        if self.score < 0:
            self.score = 0

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        score_text = self.font.render("Score: " + str(int(self.score)), True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        return True

    @staticmethod
    def get_distance(point1, point2):
        return math.hypot(point1[0] - point2[0], point1[1] - point2[1])


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
        if keys[pygame.K_UP]:
            thrust.y = -1
        if keys[pygame.K_DOWN]:
            thrust.y = 1
        if keys[pygame.K_LEFT]:
            thrust.x = -1
        if keys[pygame.K_RIGHT]:
            thrust.x = 1
        if thrust.length() > 0:
            thrust.scale_to_length(self.max_speed)
        self.velocity += thrust
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target_center):
        movement = pygame.math.Vector2(target_center[0] - self.rect.centerx, target_center[1] - self.rect.centery)
        if movement.length() > 0:
            movement.scale_to_length(self.speed)
        self.rect.move_ip(movement)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        running = game.run(None)
        game.clock.tick(FPS)
    pygame.quit()
    sys.exit()
