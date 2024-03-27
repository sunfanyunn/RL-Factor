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
        self.score = 0

        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.red_puck.update(self.agent.rect.center)
        self.check_collisions()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def check_collisions(self):
        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()
        distance_to_red = pygame.math.Vector2(self.agent.rect.centerx - self.red_puck.rect.centerx,
                                            self.agent.rect.centery - self.red_puck.rect.centery).length()
        if distance_to_red <= self.red_puck.image.get_width() // 2:
            self.score -= RED_PENALTY_FACTOR


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 12
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5
        self.add_collider()

    def add_collider(self):
        self.radius = 25
        self.radius = int(math.sqrt((self.image.get_width() / 2) ** 2 + (self.image.get_height() / 2) ** 2))

    def apply_thrusters(self, keys):
        acceleration = pygame.math.Vector2(0, 0)
        if keys[pygame.K_UP]:
            acceleration.y = -1
        if keys[pygame.K_DOWN]:
            acceleration.y = 1
        if keys[pygame.K_LEFT]:
            acceleration.x = -1
        if keys[pygame.K_RIGHT]:
            acceleration.x = 1

        self.velocity += acceleration
        self.velocity = self.velocity.limit(self.max_speed)

    def update(self):
        self.rect.centerx += int(self.velocity.x)
        self.rect.centery += int(self.velocity.y)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 30
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        target_vector = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if target_vector.length() > 0:
            target_vector.scale_to_length(self.speed)
            self.rect.center += target_vector


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.center = (random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius))

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
