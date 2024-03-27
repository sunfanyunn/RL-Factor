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

        # Create sprites
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.red_puck = RedPuck()

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent, self.green_dot, self.red_puck)

        self.green_dot.randomize_position()

    def run(self, event):
        """Implement the game loop here, given the pygame event"""
        if event.type == pygame.QUIT:
            return False

        # Handle input
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        # Update the game state
        self.all_sprites.update()

        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.score += GREEN_REWARD
            self.green_dot.randomize_position()

        # Calculate distance from red puck
        distance_to_red = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)
        self.score -= int(RED_PENALTY_FACTOR * max(0, (60 - distance_to_red)))

        # Render
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # Display score
        self.display_score(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)
        return True

    def display_score(self, surface):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', 1, WHITE)
        surface.blit(text, (10, 10))


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the agent"""
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        x, y = self.velocity
        if keys[pygame.K_LEFT]:
            x -= 1
        if keys[pygame.K_RIGHT]:
            x += 1
        if keys[pygame.K_UP]:
            y -= 1
        if keys[pygame.K_DOWN]:
            y += 1

        self.velocity = pygame.math.Vector2(x, y).normalize() * self.max_speed

    def update(self):
        """Update the agent's position"""
        self.rect.move_ip(self.velocity)
        self.rect.clamp_ip(self.screen.get_rect())


class RedPuck(pygame.sprite.Sprite):
    """Class representing the red puck obstacle"""

    def __init__(self):
        """Initialize the red puck"""
        super().__init__()
        radius = 30
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 2

    def update(self, target):
        if self.rect.centerx < target.rect.centerx:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if self.rect.centery < target.rect.centery:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the green dot"""
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

    def randomize_position(self):
        """Randomize the green dot's position"""
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def update(self):
        pass # Green dot does not move on its own


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
    sys.exit()
