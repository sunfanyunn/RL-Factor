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
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        if not event or event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        agent_center = pygame.math.Vector2(self.agent.rect.center)
        green_dot_center = pygame.math.Vector2(self.green_dot.rect.center)
        red_puck_center = pygame.math.Vector2(self.red_puck.rect.center)

        close_to_green = max(0, GREEN_REWARD - agent_center.distance_to(green_dot_center) * 0.2)
        close_to_red = max(0, (agent_center.distance_to(red_puck_center) - 30) * RED_PENALTY_FACTOR)
        self.score += int(close_to_green - close_to_red)

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
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
        acceleration = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            acceleration.x = -1
        if keys[pygame.K_RIGHT]:
            acceleration.x = 1
        if keys[pygame.K_UP]:
            acceleration.y = -1
        if keys[pygame.K_DOWN]:
            acceleration.y = 1
        self.velocity += acceleration
        if self.velocity.magnitude() > self.max_speed:
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

class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 15
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        move = pygame.math.Vector2(target) - self.rect.center
        if move.length() > 0:
            move = move.normalize() * self.speed
        self.rect.move_ip(move)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect(center=(random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5)))

    def randomize_position(self):
        self.rect.center = (random.randint(5, WIDTH - 5), random.randint(5, HEIGHT - 5))

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break

        if not running:
            break

        running = game.run(None)
    pygame.quit()
    sys.exit()


