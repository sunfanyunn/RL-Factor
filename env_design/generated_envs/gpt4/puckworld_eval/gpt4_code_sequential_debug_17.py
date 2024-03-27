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
        self.agent = Agent(self)
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.all_sprites.add(self.green_dot)
        self.all_sprites.add(self.red_puck)
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def run(self, event):
        self.agent.apply_thrusters(pygame.key.get_pressed())
        self.agent.update()
        self.green_dot.update()
        self.red_puck.update(self.agent.rect.center)
        if pygame.sprite.collide_rect(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()
        distance = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
        if distance < 100:
            self.score -= RED_PENALTY_FACTOR * (100 - distance)
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.show_score()
        pygame.display.flip()
        self.clock.tick(FPS)
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        return True

    def show_score(self):
        score_surf = self.font.render(f'Score: {int(self.score)}', True, WHITE)
        self.screen.blit(score_surf, (10, 10))

class Agent(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.velocity = [0, 0]
        self.max_speed = 5
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (12, 12), 12)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def apply_thrusters(self, keys):
        x, y = self.velocity
        if keys[pygame.K_UP]:
            y -= 1
        if keys[pygame.K_DOWN]:
            y += 1
        if keys[pygame.K_LEFT]:
            x -= 1
        if keys[pygame.K_RIGHT]:
            x += 1
        x = max(min(x, self.max_speed), -self.max_speed)
        y = max(min(y, self.max_speed), -self.max_speed)
        self.velocity = [x, y]

    def update(self):
        self.rect.move_ip(*self.velocity)
        self.rect.clamp_ip(self.game.screen.get_rect())

class RedPuck(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 60
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.speed = 2

    def update(self, target):
        direction_vector = [target[0] - self.rect.centerx, target[1] - self.rect.centery]
        distance = math.hypot(*direction_vector)
        if distance > 0:
            normalized_direction = [direction_vector[0] / distance, direction_vector[1] / distance]
        else:
            normalized_direction = [0, 0]
        self.rect.centerx += int(self.speed * normalized_direction[0])
        self.rect.centery += int(self.speed * normalized_direction[1])

class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GREEN, (self.radius, self.radius), self.radius)
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
        for event in pygame.event.get():
            if not game.run(event):
                running = False
    pygame.quit()
    sys.exit()

