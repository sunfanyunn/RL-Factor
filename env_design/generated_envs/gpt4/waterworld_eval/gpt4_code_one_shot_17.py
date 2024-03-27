
import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60
CIRCLE_RADIUS = 10

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Game:
    def __init__(self):
        """
        Initialize the game window, clock, game_over status, and score.
        Create sprite groups for all game objects.
        agent: The player-controlled sprite.
        circles: A group of all circles in the game.
        
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WaterWorld Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.circles = pygame.sprite.Group()
        self.agent = Agent()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        num_circles = GRID_WIDTH * GRID_HEIGHT // 10
        for _ in range(num_circles):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle = Circle(color)
            new_circle.rect.topleft = (x, y)
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                break

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        for circle in self.circles:
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                elif circle.color == RED:
                    self.score -= 1
                color = GREEN if random.choice([True, False]) else RED
                self.circles.remove(circle)
                self.spawn_circle(color)
        self.circles.update()

        remaining_green = any(c.color == GREEN for c in self.circles)
        if not remaining_green:
            self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.score = 0
        self.game_over = False
        self.circles.empty()
        self.agent.reset()
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if self.game_over and event.key == pygame.K_r:
                self.reset_game()
        return True

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.show_message(f'Score: {self.score}', 20, (10, 10))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', 36, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

    def show_message(self, message, size=36, position=(WIDTH // 2, HEIGHT // 2)):
        """
        Display a message on the screen.
        """
        font = pygame.font.Font(None, size)
        text_surface = font.render(message, True, (0, 0, 0))
        rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, rect)

    def run(self, event):
        """
        Main game loop.
        """
        self.handle_events(event)
        if not self.game_over:
            self.agent.update()
            self.update_circles()
        self.render_game()
        self.clock.tick(FPS)
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        self.direction = pygame.Vector2()

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        keys = pygame.key.get_pressed()
        self.direction.x, self.direction.y = 0, 0
        if keys[pygame.K_LEFT]:
            self.direction.x = -GRID_SIZE
        elif keys[pygame.K_RIGHT]:
            self.direction.x = GRID_SIZE
        if keys[pygame.K_UP]:
            self.direction.y = -GRID_SIZE
        elif keys[pygame.K_DOWN]:
            self.direction.y = GRID_SIZE

        self.move(self.direction.x, self.direction.y)

        # Keep the agent within the window bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
        self.speed = random.randint(1, 3)

    def reset(self):
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.rect.topleft = (x, y)
        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
        self.speed = random.randint(1, 3)

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction.y *= -1

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        game.run(event)
        running = game.handle_events(event)
    pygame.quit()

