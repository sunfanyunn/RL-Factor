import pygame
import sys
import random

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
        self.font = pygame.font.Font(None, 34)
        self.score = 0

        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.all_sprites.update(self.agent.rect)

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()
            self.score += GREEN_REWARD

        dist_to_red_puck = pygame.math.Vector2(self.agent.rect.centerx - self.red_puck.rect.centerx,
                                               self.agent.rect.centery - self.red_puck.rect.centery).length()
        if dist_to_red_puck < WIDTH // 2:
            self.score -= int(RED_PENALTY_FACTOR * (1 / max(dist_to_red_puck, 1)))

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

        self.clock.tick(FPS)
        return event.type != pygame.QUIT


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (25, 25), 25)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        thrust = pygame.math.Vector2(0, 0)
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


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 15
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius),
                                               random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target_rect):
        direction = pygame.math.Vector2(target_rect.center) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 5
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        radius = 5
        self.rect.center = (random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius))

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
