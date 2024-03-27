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
        self.font = pygame.font.Font(None, 36)
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)
        self.green_dot.randomize_position()
        self.red_puck.set_agent(self.agent)

    def run(self, event):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)
            self.all_sprites.update()
            if self.agent.rect.colliderect(self.green_dot.rect):
                self.green_dot.randomize_position()
                self.score += GREEN_REWARD
            penalty = self.calculate_penalty()
            self.score -= penalty * self.clock.get_time() / 1000
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            score_text = self.font.render(f'Score: {max(self.score, 0)}', True, WHITE)
            self.screen.blit(score_text, (10, 10))
            pygame.display.flip()

    def calculate_penalty(self):
        agent_distance_to_red = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
        return RED_PENALTY_FACTOR * max(100 - agent_distance_to_red, 0) / 100


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (25, 25), 25)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.max_speed = 5
        self.velocity = pygame.math.Vector2(0, 0)

    def apply_thrusters(self, keys):
        self.velocity.update(0, 0)
        if keys[pygame.K_UP]:
            self.velocity.y = -self.max_speed
        if keys[pygame.K_DOWN]:
            self.velocity.y = self.max_speed
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.max_speed
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.max_speed

    def update(self):
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 15
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect()

    def set_agent(self, agent):
        self.agent = agent

    def update(self):
        if self.agent:
            target = self.agent.rect.center
            direction_vector = pygame.math.Vector2(target) - self.rect.center
            if direction_vector.length() > 0:
                direction_vector = direction_vector.normalize() * self.speed
            self.rect.move_ip(direction_vector.x, direction_vector.y)
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 5
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (radius, radius), radius)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def update(self):
        pass


if __name__ == '__main__':
    game = Game()
    result = game.run(None)
    if not result:
        pygame.quit()
        sys.exit()