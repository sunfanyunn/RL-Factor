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

GREEN_REWARD_DISTANCE = 10
RED_PENALTY_DISTANCE = 30
SCORE_REWARD = 5
SCORE_PENALTY = 1


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
        self.font = pygame.font.SysFont(None, 36)

    def run(self, event):
        running = True
        if event.type == pygame.QUIT:
            return False

        self.screen.fill(BLACK)

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        score_text = self.font.render('Score: ' + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

        self.agent.draw(self.screen)
        self.green_dot.draw(self.screen)
        self.red_puck.draw(self.screen)

        self.check_collisions()

        pygame.display.flip()
        self.clock.tick(FPS)
        return running

    def check_collisions(self):
        if self.agent.rect.colliderect(self.green_dot.rect):
            self.score += SCORE_REWARD
            self.green_dot.randomize_position(WIDTH, HEIGHT)

        if pygame.sprite.collide_circle(self.agent, self.red_puck):
            self.score -= SCORE_PENALTY


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 12
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
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

        thrust.normalize_ip()
        self.velocity += thrust
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity.x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity.y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 30
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)))
        self.speed = 0.5

    def update(self, target_pos):
        target_vector = pygame.Vector2(target_pos) - self.rect.center
        if target_vector.length() > 0:
            target_vector.scale_to_length(self.speed)
            self.rect.move_ip(target_vector.x, target_vector.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius)))

    def randomize_position(self, width, height):
        self.rect.center = (random.randint(self.radius, width - self.radius), random.randint(self.radius, height - self.radius))

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
