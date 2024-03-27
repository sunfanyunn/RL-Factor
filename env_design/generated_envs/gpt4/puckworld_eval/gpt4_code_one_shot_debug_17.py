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
        self.font = pygame.font.SysFont(None, 36)

        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

        self.agent_group = pygame.sprite.Group(self.agent)
        self.green_dot_group = pygame.sprite.Group(self.green_dot)
        self.red_puck_group = pygame.sprite.Group(self.red_puck)

        self.score = 0
        self.green_dot.randomize_position()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        score_increase = 0

        if pygame.sprite.spritecollide(self.agent, self.green_dot_group, True):
            self.green_dot.randomize_position()
            self.green_dot_group.add(self.green_dot)
            score_increase = GREEN_REWARD

        distance_to_green = math.hypot(
            self.agent.rect.centerx - self.green_dot.rect.centerx,
            self.agent.rect.centery - self.green_dot.rect.centery
        )
        score_increase += int(GREEN_REWARD / (1 + distance_to_green))

        distance_to_red = math.hypot(
            self.agent.rect.centerx - self.red_puck.rect.centerx,
            self.agent.rect.centery - self.red_puck.rect.centery
        )
        score_decrease = int(RED_PENALTY_FACTOR * (1 + distance_to_red))

        self.score += score_increase - score_decrease

        self.screen.fill(BLACK)
        self.agent_group.draw(self.screen)
        self.green_dot_group.draw(self.screen)
        self.red_puck_group.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        self.clock.tick(FPS)

        return True

class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        self.velocity.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 0.5
        self.velocity.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 0.5
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

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

    def __init__(self):
        super().__init__()
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.speed = 1

    def update(self, target):
        target_vector = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if target_vector.length() > 0:
            target_vector.scale_to_length(self.speed)
        self.rect.move_ip(target_vector)

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
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            running = game.run(event)
    pygame.quit()
    sys.exit()
