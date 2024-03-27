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
        self.agent = Agent(self.screen)
        self.green_dot = GreenDot()
        self.red_puck = RedPuck(self.screen)
        self.green_dot.randomize_position()

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        agent_distance = math.hypot(
            self.agent.rect.centerx - self.green_dot.rect.centerx,
            self.agent.rect.centery - self.green_dot.rect.centery
        )
        puck_distance = math.hypot(
            self.agent.rect.centerx - self.red_puck.rect.centerx,
            self.agent.rect.centery - self.red_puck.rect.centery
        )

        self.score += GREEN_REWARD / max(agent_distance, 1) - RED_PENALTY_FACTOR / max(puck_distance, 1)

        if self.agent.rect.colliderect(self.green_dot.rect):
            self.green_dot.randomize_position()

        self.screen.fill(BLACK)
        self.green_dot.draw(self.screen)
        self.red_puck.draw(self.screen)
        self.agent.draw(self.screen)

        score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (5, 5))

        pygame.display.flip()
        self.clock.tick(FPS)

        return True

class Agent(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (25 // 2, 25 // 2), 25 // 2)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        if keys[pygame.K_LEFT]:
            self.velocity.x = max(self.velocity.x - 1, -self.max_speed)
        if keys[pygame.K_RIGHT]:
            self.velocity.x = min(self.velocity.x + 1, self.max_speed)
        if keys[pygame.K_UP]:
            self.velocity.y = max(self.velocity.y - 1, -self.max_speed)
        if keys[pygame.K_DOWN]:
            self.velocity.y = min(self.velocity.y + 1, self.max_speed)

    def update(self):
        self.rect.centerx += round(self.velocity.x)
        self.rect.centery += round(self.velocity.y)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity.x = -self.velocity.x
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity.y = -self.velocity.y

        self.rect.clamp_ip(self.screen.get_rect())

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class RedPuck(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 1

    def update(self, target):
        target_vector = pygame.math.Vector2(target)
        puck_vector = pygame.math.Vector2(self.rect.center)
        if target_vector != puck_vector:
            direction_vector = (target_vector - puck_vector).normalize()
            self.rect.centerx += direction_vector.x * self.speed
            self.rect.centery += direction_vector.y * self.speed

        self.rect.clamp_ip(self.screen.get_rect())

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.center = (random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
