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
        self.font = pygame.font.Font(None, 36)

    def run(self, event):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)
            self.agent.update()
            self.red_puck.update(self.agent.rect.center)
            self.green_dot.update()

            self.screen.fill(BLACK)
            self.agent.draw(self.screen)
            self.red_puck.draw(self.screen)
            self.green_dot.draw(self.screen)

            distance_to_green = math.hypot(self.agent.rect.centerx - self.green_dot.rect.centerx, self.agent.rect.centery - self.green_dot.rect.centery)
            if distance_to_green < 12 + 5:
                self.score += GREEN_REWARD
                self.green_dot.randomize_position()

            distance_to_red = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
            self.score -= RED_PENALTY_FACTOR / max(distance_to_red, 10)

            score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
            self.screen.blit(score_text, (5, 5))

            pygame.display.flip()
            self.clock.tick(FPS)

        return running


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
            self.velocity.x -= 0.1
        if keys[pygame.K_RIGHT]:
            self.velocity.x += 0.1
        if keys[pygame.K_UP]:
            self.velocity.y -= 0.1
        if keys[pygame.K_DOWN]:
            self.velocity.y += 0.1

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

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        direction = pygame.math.Vector2(target[0] - self.rect.centerx, target[1] - self.rect.centery)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect(center=(random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5)))

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
        if event.type == pygame.QUIT:
            running = False
        elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
            running = game.run(event)
    pygame.quit()
    sys.exit()
