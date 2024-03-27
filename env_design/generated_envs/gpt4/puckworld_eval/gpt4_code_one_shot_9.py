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
        self.font = pygame.font.Font(None, 34)
        self.score = 0

        self.agent = Agent()
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.all_sprites.add(self.green_dot)
        self.all_sprites.add(self.red_puck)

    def run(self, event):
        """Game loop; updates game state, redraws the screen, checks for game over."""
        keys = pygame.key.get_pressed()
        self.agent.apply_thrusters(keys)

        # Update sprite positions
        self.all_sprites.update()

        # Check for collisions
        if pygame.sprite.collide_circle(self.agent, self.green_dot):
            self.green_dot.randomize_position()
            self.score += GREEN_REWARD

        # Calculate distance to red_puck
        dist_to_red_puck = math.hypot(self.agent.rect.centerx - self.red_puck.rect.centerx, self.agent.rect.centery - self.red_puck.rect.centery)

        # Penalize based on proximity to red_puck
        self.score -= int(RED_PENALTY_FACTOR * (1 / max(dist_to_red_puck, 1)))
        self.red_puck.update(self.agent.rect.center)

        # Draw everything
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # Display score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Check for game quit event
        if event.type == pygame.QUIT:
            return False

        # Cap the frame rate
        self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the agent."""
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed = 5

    def apply_thrusters(self, keys):
        thrust = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            thrust.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            thrust.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            thrust.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
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
        """Initialize the red puck."""
        super().__init__()
        radius = 30
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(radius, WIDTH - radius), random.randint(radius, HEIGHT - radius)))
        self.speed = 1

    def update(self, target):
        direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.scale_to_length(self.speed)
        self.rect.move_ip(direction)


class GreenDot(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize the green dot."""
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
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
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)

    pygame.quit()
    sys.exit()
