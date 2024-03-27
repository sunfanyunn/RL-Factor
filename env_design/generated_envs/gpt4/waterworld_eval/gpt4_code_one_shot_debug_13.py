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
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.score = 0
        self.game_over = False
        self.green_circles_count = 0
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        circle = Circle(color)
        while True:
            circle.reset()
            if not pygame.sprite.spritecollideany(circle, self.circles):
                self.circles.add(circle)
                if color == GREEN:
                    self.green_circles_count += 1
                break

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        collided_circles = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collided_circles:
            if circle.color == GREEN:
                self.score += 1
                self.green_circles_count -= 1
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))

    def reset_game(self):
        """
        Reset the game state.
        """
        self.circles.empty()
        self.score = 0
        self.green_circles_count = 0
        self.agent.reset()
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if not self.game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.agent.move((0, -1))
            elif event.key == pygame.K_DOWN:
                self.agent.move((0, 1))
            elif event.key == pygame.K_LEFT:
                self.agent.move((-1, 0))
            elif event.key == pygame.K_RIGHT:
                self.agent.move((1, 0))
        if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        for entity in self.circles:
            self.screen.blit(entity.image, entity.rect)
        self.screen.blit(self.agent.image, self.agent.rect)

        score_text = "Score: " + str(self.score)
        self.show_message(score_text, 20, (5, 5))

        if self.game_over:
            self.show_message("Game Over! Press 'R' to Restart", 40, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

    def show_message(self, message, size, position):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, BLUE)
        self.screen.blit(text_surface, position)

    def run(self, event):
        """
        Main game loop.
        """
        self.handle_events(event)
        if not self.game_over:
            self.agent.update()
            self.circles.update()
            self.update_circles()
            self.render_game()
            if self.green_circles_count == 0:
                self.game_over = True
        else:
            self.render_game()
        self.clock.tick(FPS)
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the agent sprite.
        
        """
        super().__init__()
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        """
        Reset the agent's position.
        """
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        """
        Move the agent in the specified direction.
        """
        x, y = direction
        self.rect.move_ip(x * GRID_SIZE, y * GRID_SIZE)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def update(self):
        """
        Update method for the agent (unused in this example).
        """
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        """
        Initialize a circle sprite with a specified color
        """
        super().__init__()
        self.color = color
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()
        self.direction = [random.choice([-1, 1]) * random.uniform(0.5, 3) for _ in range(2)]

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.direction = [random.choice([-1, 1]) * random.uniform(0.5, 3) for _ in range(2)]

    def update(self):
        """
        Update the circle's position.
        """
        self.move_smoothly()

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        self.rect.move_ip(*self.direction)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction[0] *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.direction[1] *= -1

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            running = game.run(event)
    pygame.quit()
