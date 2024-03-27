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

AGENT_RADIUS = 15
RED_PUCK_RADIUS = 30
GREEN_DOT_RADIUS = 5

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)
        self.font = pygame.font.SysFont(None, 36)
        self.score = 0

    def run(self, event):
        running = True
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.all_sprites.update()
        self.check_collisions()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_score()

        pygame.display.flip()
        self.clock.tick(FPS)
        return running

    def check_collisions(self):
        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()
            self.score += GREEN_REWARD
        if pygame.sprite.collide_circle(self.agent, self.red_puck):
            self.score -= RED_PENALTY_FACTOR * self.red_puck.get_distance(self.agent)

    def draw_score(self):
        score_surf = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_surf, (10, 10))


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2 * AGENT_RADIUS, 2 * AGENT_RADIUS), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (AGENT_RADIUS, AGENT_RADIUS), AGENT_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        acceleration = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            acceleration.x -= 1
        if keys[pygame.K_RIGHT]:
            acceleration.x += 1
        if keys[pygame.K_UP]:
            acceleration.y -= 1
        if keys[pygame.K_DOWN]:
            acceleration.y += 1
        if acceleration.length() > 0:
            acceleration.scale_to_length(self.max_speed)
        self.velocity += acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        if keys[pygame.K_SPACE]:
            self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2 * RED_PUCK_RADIUS, 2 * RED_PUCK_RADIUS), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (RED_PUCK_RADIUS, RED_PUCK_RADIUS), RED_PUCK_RADIUS)
        self.rect = self.image.get_rect(center=(random.randint(RED_PUCK_RADIUS, WIDTH - RED_PUCK_RADIUS), random.randint(RED_PUCK_RADIUS, HEIGHT - RED_PUCK_RADIUS)))
        self.speed = 1

    def update(self):
        direction = pygame.math.Vector2(self.agent.rect.center) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)

    def get_distance(self, target):
        return pygame.math.Vector2(target.rect.center).distance_to(self.rect.center) // 10


class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2 * GREEN_DOT_RADIUS, 2 * GREEN_DOT_RADIUS), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (GREEN_DOT_RADIUS, GREEN_DOT_RADIUS), GREEN_DOT_RADIUS)
        self.rect = self.image.get_rect(center=(random.randint(GREEN_DOT_RADIUS, WIDTH - GREEN_DOT_RADIUS), random.randint(GREEN_DOT_RADIUS, HEIGHT - GREEN_DOT_RADIUS)))

    def randomize_position(self):
        self.rect.center = (random.randint(GREEN_DOT_RADIUS, WIDTH - GREEN_DOT_RADIUS), random.randint(GREEN_DOT_RADIUS, HEIGHT - GREEN_DOT_RADIUS))

    def update(self):
        pass

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.NOEVENT:
            event = pygame.event.Event(pygame.USEREVENT)
        running = game.run(event)
    pygame.quit()
    sys.exit()
