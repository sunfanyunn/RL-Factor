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
        self.agent = Agent(self.screen)
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
        self.score = 0
        self.font = pygame.font.SysFont(None, 24)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        distance = self.get_distance(self.agent.rect.center, self.green_dot.rect.center)
        self.score += max(0, int(GREEN_REWARD / (distance + 1)))
        distance_to_red_puck = self.get_distance(self.agent.rect.center, self.red_puck.rect.center)
        self.score -= int(RED_PENALTY_FACTOR * max(0, (150 - distance_to_red_puck)))

        if distance < 25:
            self.green_dot.randomize_position()

        self.red_puck.update(self.agent.rect.center)
        self.green_dot.update()
        self.agent.update()

        self.screen.fill(BLACK)
        self.agent.draw(self.screen)
        self.green_dot.draw(self.screen)
        self.red_puck.draw(self.screen)

        score_text = self.font.render('Score: {}'.format(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    @staticmethod
    def get_distance(pos1, pos2):
        return math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])


class Agent(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = [0, 0]
        self.max_speed = 5
        self.screen = screen

    def apply_thrusters(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity[0] = -self.max_speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity[0] = self.max_speed
        else:
            self.velocity[0] = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity[1] = -self.max_speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity[1] = self.max_speed
        else:
            self.velocity[1] = 0

    def update(self):
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(self.screen.get_rect())

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 15
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        delta_x = target[0] - self.rect.centerx
        delta_y = target[1] - self.rect.centery
        distance = math.hypot(delta_x, delta_y)
        if distance != 0:
            move_x = delta_x / distance * self.speed
            move_y = delta_y / distance * self.speed
            self.rect.centerx += int(move_x)
            self.rect.centery += int(move_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.x = random.randint(0, WIDTH - 10)
        self.rect.y = random.randint(0, HEIGHT - 10)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
    sys.exit()
