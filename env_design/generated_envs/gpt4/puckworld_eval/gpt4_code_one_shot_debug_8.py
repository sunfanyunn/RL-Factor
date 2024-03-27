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
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)
            self.agent.update()
            self.red_puck.update(self.agent.rect.center)

            agent_distance = math.hypot(
                self.agent.rect.centerx - self.green_dot.rect.centerx,
                self.agent.rect.centery - self.green_dot.rect.centery
            )
            puck_distance = math.hypot(
                self.agent.rect.centerx - self.red_puck.rect.centerx,
                self.agent.rect.centery - self.red_puck.rect.centery
            )

            if agent_distance < self.green_dot.radius + self.agent.radius:
                self.green_dot.randomize_position()
                self.score += GREEN_REWARD

            if puck_distance < self.red_puck.radius + self.agent.radius:
                self.score -= RED_PENALTY_FACTOR

            self.screen.fill(BLACK)
            self.green_dot.draw(self.screen)
            self.red_puck.draw(self.screen)
            self.agent.draw(self.screen)

            score_text = self.font.render(f'Score: {self.score}', True, WHITE)
            self.screen.blit(score_text, (5, 5))

            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 12.5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        thrust = pygame.Vector2(0, 0)
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
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 30
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)))
        self.speed = 1

    def update(self, target):
        target_vector = pygame.Vector2(target)
        direction_vector = target_vector - pygame.Vector2(self.rect.center)
        if direction_vector.length() > 0:
            direction_vector.scale_to_length(self.speed)
        self.rect.move_ip(direction_vector)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.center = (random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


if __name__ == "__main__":
    game = Game()
    game.run()
