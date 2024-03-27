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
        self.font = pygame.font.SysFont(None, 36)
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        self.screen.fill(BLACK)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()

        self.red_puck.update(self.agent.rect.center)

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()

        distance_to_red = math.hypot(self.red_puck.rect.centerx - self.agent.rect.centerx, self.red_puck.rect.centery - self.agent.rect.centery)
        if distance_to_red > 0:
            self.score -= RED_PENALTY_FACTOR / distance_to_red

        self.sprites.update()
        self.sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)
        return True

class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = [0, 0]
        self.max_speed = 5

    def apply_thrusters(self, keys):
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= 1
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += 1
        if keys[pygame.K_UP]:
            self.velocity[1] -= 1
        if keys[pygame.K_DOWN]:
            self.velocity[1] += 1
        for i in (0, 1):
            if abs(self.velocity[i]) > self.max_speed:
                self.velocity[i] = self.max_speed * (self.velocity[i] / abs(self.velocity[i]))
            self.velocity[i] *= 0.9

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def update(self):
        self.rect.move_ip(self.velocity)


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 20
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        if target:
            target_x, target_y = target
            puck_x, puck_y = self.rect.center
            direction = math.atan2(target_y - puck_y, target_x - puck_x)
            self.rect.x += round(self.speed * math.cos(direction))
            self.rect.y += round(self.speed * math.sin(direction))


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
        running = game.run(None)
    pygame.quit()
    sys.exit()