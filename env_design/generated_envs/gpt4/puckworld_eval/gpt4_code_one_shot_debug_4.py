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
        """Initialize the game
        agent: the player's character
        green_dot: the target for the agent
        red_puck: the obstacle for the agent
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.score = 0

        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.green_dot.update()

        green_distance = self.agent.get_distance_to(self.green_dot.rect.center)
        red_distance = self.agent.get_distance_to(self.red_puck.rect.center)
        self.score += int(GREEN_REWARD / max(green_distance, 1)) - int(RED_PENALTY_FACTOR / max(red_distance, 1))

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()

        self.red_puck.update(self.agent.rect.center)

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        score_text = pygame.font.Font(None, 36).render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()
        return True

    def signal_handler(self, signal):
        pygame.quit()
        sys.exit()


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = [0, 0]
        self.max_speed = 5
        self.radius = 12

    def apply_thrusters(self, keys):
        if keys[pygame.K_UP]:
            self.velocity[1] -= 1
        if keys[pygame.K_DOWN]:
            self.velocity[1] += 1
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= 1
        if keys[pygame.K_RIGHT]:
            self.velocity[0] += 1

        speed = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.velocity[0] *= scale
            self.velocity[1] *= scale

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def get_distance_to(self, target):
        return math.hypot(target[0] - self.rect.centerx, target[1] - self.rect.centery)


class GreenDot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.randomize_position()
        self.radius = 5

    def randomize_position(self):
        self.rect.x = random.randint(0, WIDTH - 10)
        self.rect.y = random.randint(0, HEIGHT - 10)

    def update(self):
        pass


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 60  # Increased size
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.radius = radius
        self.speed = 2

    def update(self, target):
        target_vector = [target[0] - self.rect.centerx, target[1] - self.rect.centery]
        distance = math.sqrt(target_vector[0] ** 2 + target_vector[1] ** 2)
        if distance > 0:
            target_vector[0] *= self.speed / distance
            target_vector[1] *= self.speed / distance
            self.rect.x += target_vector[0]
            self.rect.y += target_vector[1]

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()