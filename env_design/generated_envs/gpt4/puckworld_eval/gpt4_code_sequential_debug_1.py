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
        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

    def run(self, event):
        self.clock.tick(FPS)
        self.screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)
        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent)

        self.score += self.agent.check_collision(self.green_dot, self.red_puck)

        score_text = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()
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
        acceleration = pygame.math.Vector2()
        if keys[pygame.K_LEFT]:
            acceleration.x -= 1
        if keys[pygame.K_RIGHT]:
            acceleration.x += 1
        if keys[pygame.K_UP]:
            acceleration.y -= 1
        if keys[pygame.K_DOWN]:
            acceleration.y += 1
        if acceleration.length() > 0:
            acceleration.scale_to_length(0.5)
            self.velocity += acceleration
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

    def update(self):
        self.rect.move_ip(self.velocity.x, self.velocity.y)
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = -self.velocity.x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity.x = -self.velocity.x
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = -self.velocity.y
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity.y = -self.velocity.y

    def check_collision(self, green_dot, red_puck):
        score_change = 0
        green_distance = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(green_dot.rect.center)
        if green_distance.length() < 25:
            score_change += GREEN_REWARD
            green_dot.randomize_position()
        else:
            score_change -= 1 / (1 + green_distance.length_squared())

        red_distance = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(red_puck.rect.center)
        if red_distance.length() < 60:
            score_change -= RED_PENALTY_FACTOR / (1 + red_distance.length_squared())
        return score_change


class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(random.randrange(WIDTH), random.randrange(HEIGHT)))
        self.speed = 2

    def update(self, target):
        direction = pygame.math.Vector2(target.rect.center) - pygame.math.Vector2(self.rect.center)
        if direction.length_squared() > 0:
           direction.scale_to_length(self.speed)
           self.rect.move_ip(direction.x, direction.y)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        pygame.draw.circle(self.image, GREEN, (5, 5), 5)
        self.rect = self.image.get_rect(center=(random.randrange(WIDTH), random.randrange(HEIGHT)))

    def randomize_position(self):
        self.rect.x = random.randrange(25, WIDTH - 25)
        self.rect.y = random.randrange(25, HEIGHT - 25)

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
