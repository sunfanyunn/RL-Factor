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
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        self.screen.fill(BLACK)
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        distance_to_green_dot = self.calculate_distance(self.agent.rect, self.green_dot.rect)
        self.score += (GREEN_REWARD / distance_to_green_dot) if distance_to_green_dot > 0 else 0

        distance_to_red_puck = self.calculate_distance(self.agent.rect, self.red_puck.rect)
        self.score -= (distance_to_red_puck * RED_PENALTY_FACTOR) if distance_to_red_puck > 0 else 0

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()
        self.red_puck.update(self.agent.rect)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.display_score()
        pygame.display.flip()
        self.clock.tick(FPS)

        return event.type != pygame.QUIT

    def calculate_distance(self, rect1, rect2):
        x1 = rect1.centerx
        y1 = rect1.centery
        x2 = rect2.centerx
        y2 = rect2.centery
        return math.hypot(x2 - x1, y2 - y1)

    def display_score(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render("Score: {:0.1f}".format(self.score), True, WHITE)
        self.screen.blit(text, (10, 10))


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        acceleration = 0.5
        if keys[pygame.K_LEFT]:
            self.velocity.x -= acceleration
        if keys[pygame.K_RIGHT]:
            self.velocity.x += acceleration
        if keys[pygame.K_UP]:
            self.velocity.y -= acceleration
        if keys[pygame.K_DOWN]:
            self.velocity.y += acceleration

        if self.velocity.magnitude() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        direction = pygame.math.Vector2(target.center) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction.x, direction.y)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 5
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))

    def randomize_position(self):
        radius = 5
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        running = game.run(None)
    pygame.quit()
    sys.exit()

