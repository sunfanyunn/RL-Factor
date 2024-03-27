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
        self.agent = Agent(self)
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)
        self.green_dot.randomize_position()

    def run(self, event):
        """please implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.agent.update()
        self.red_puck.update(self.agent)
        self.green_dot.update()

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()

        distance_to_red = math.hypot(
            self.agent.rect.centerx - self.red_puck.rect.centerx,
            self.agent.rect.centery - self.red_puck.rect.centery)
        self.score -= int(RED_PENALTY_FACTOR * max(0, (120 - distance_to_red)))

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        self.display_score()

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def display_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(text, (10, 10))


class Agent(pygame.sprite.Sprite):

    def __init__(self, game):
        """Initialize the agent"""
        super().__init__()
        self.game = game
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        x, y = 0, 0
        if keys[pygame.K_LEFT]:
            x -= 1
        if keys[pygame.K_RIGHT]:
            x += 1
        if keys[pygame.K_UP]:
            y -= 1
        if keys[pygame.K_DOWN]:
            y += 1
        if x or y:
            thrust = pygame.math.Vector2(x, y).normalize() * 0.5
            self.velocity += thrust
            if self.velocity.magnitude() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(self.game.screen.get_rect())

    def update(self):
        pass


class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius = 60  # Increased size
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius),
                                                random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        if self.rect.centerx < target.rect.centerx:
            self.rect.x += self.speed
        elif self.rect.centerx > target.rect.centerx:
            self.rect.x -= self.speed

        if self.rect.centery < target.rect.centery:
            self.rect.y += self.speed
        elif self.rect.centery > target.rect.centery:
            self.rect.y -= self.speed


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

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
