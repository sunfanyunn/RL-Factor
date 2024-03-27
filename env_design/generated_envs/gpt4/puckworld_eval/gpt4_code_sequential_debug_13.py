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
        self.sprites = pygame.sprite.Group(self.agent, self.green_dot, self.red_puck)
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)
            self.agent.update()
            self.red_puck.update(self.agent.rect.center)
            self.green_dot.update()

            if pygame.sprite.collide_circle(self.agent, self.green_dot):
                self.green_dot.randomize_position()
                self.score += GREEN_REWARD

            distance_to_red = self.agent.distance_to(self.red_puck)
            self.score -= max(distance_to_red - self.agent.radius - self.red_puck.radius, 0) * RED_PENALTY_FACTOR
            self.score = max(self.score, 0)

            self.screen.fill(BLACK)
            self.sprites.draw(self.screen)
            self.draw_score()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            break
        return True

    def draw_score(self):
        text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(text, (10, 10))



class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5
        self.radius = 12

    def apply_thrusters(self, keys):
        thrust = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            thrust.x -= 1
        if keys[pygame.K_RIGHT]:
            thrust.x += 1
        if keys[pygame.K_UP]:
            thrust.y -= 1
        if keys[pygame.K_DOWN]:
            thrust.y += 1
        self.velocity += thrust
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def distance_to(self, other_sprite):
        return pygame.math.Vector2(self.rect.center).distance_to(other_sprite.rect.center)


class RedPuck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius = 60
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.radius = radius
        self.speed = 1

    def update(self, target):
        direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect(center=(random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5)))
        self.radius = 5

    def randomize_position(self):
        self.rect.center = (random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5))

    def update(self):
        pass


if __name__ == "__main__":
    pygame.font.init()
    game = Game()
    running = game.run()
    pygame.quit()
    sys.exit()
