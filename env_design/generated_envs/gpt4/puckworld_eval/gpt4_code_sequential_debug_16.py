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
        self.red_puck = RedPuck()
        self.score = 0

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        self.screen.fill(BLACK)

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        if self.agent.rect.colliderect(self.green_dot.rect):
            self.green_dot.randomize_position()
            self.score += GREEN_REWARD

        agent_red_distance = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
        if agent_red_distance < 60:
            self.score -= int(agent_red_distance // RED_PENALTY_FACTOR)

        self.agent.draw(self.screen)
        self.green_dot.draw(self.screen)
        self.red_puck.draw(self.screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

        return True


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        if keys[pygame.K_LEFT]:
            self.velocity.x -= 1
        if keys[pygame.K_RIGHT]:
            self.velocity.x += 1
        if keys[pygame.K_UP]:
            self.velocity.y -= 1
        if keys[pygame.K_DOWN]:
            self.velocity.y += 1

        if self.velocity.x < -self.max_speed:
            self.velocity.x = -self.max_speed
        if self.velocity.x > self.max_speed:
            self.velocity.x = self.max_speed
        if self.velocity.y < -self.max_speed:
            self.velocity.y = -self.max_speed
        if self.velocity.y > self.max_speed:
            self.velocity.y = self.max_speed

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
        surface.blit(self.image, self.rect.topleft)


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        target_vector = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if target_vector.length() > 0:
            target_vector.scale_to_length(self.speed)
            self.rect.move_ip(target_vector.x, target_vector.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

    def randomize_position(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        running = game.run(None)
    pygame.quit()
    sys.exit()
