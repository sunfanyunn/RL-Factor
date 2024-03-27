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
        self.font = pygame.font.SysFont(None, 36)
        self.circles = pygame.sprite.Group()
        self.agent = Agent()
        self.agent_sprite = pygame.sprite.GroupSingle(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        circle = Circle(color)
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.circles.add(circle)

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(circle, self.agent):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(GREEN if random.random() < 0.5 else RED)

        green_circles_count = sum(circle.color == GREEN for circle in self.circles)
        if green_circles_count == 0:
            self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.game_over = False
        self.score = 0
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and not self.game_over:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.agent.move(event.key)
            elif event.key == pygame.K_r:
                self.reset_game()

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.circles.update()
        self.circles.draw(self.screen)
        self.agent_sprite.draw(self.screen)
        self.show_score()
        if self.game_over:
            self.show_message('Game Over!')
        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, BLUE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def show_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (10, 10))

    def run(self, event):
        """
        Main game loop.
        """
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
        self.render_game()
        self.clock.tick(FPS)


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

    def move(self, key):
        """
        Move the agent in the specified direction.
        """
        direction_map = {
            pygame.K_UP: (0, -GRID_SIZE),
            pygame.K_DOWN: (0, GRID_SIZE),
            pygame.K_LEFT: (-GRID_SIZE, 0),
            pygame.K_RIGHT: (GRID_SIZE, 0),
        }
        if key in direction_map:
            self.rect.move_ip(direction_map[key])
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        """
        Initialize a circle sprite with a specified color and direction
        """
        super().__init__()
        self.color = color
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def update(self):
        """
        Update the circle's position.
        """
        self.move_smoothly()


    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        if self.color == RED or self.color == GREEN:
            directions = [(GRID_SIZE, 0), (-GRID_SIZE, 0), (0, GRID_SIZE), (0, -GRID_SIZE)]
            direction = random.choice(directions)
            self.rect.move_ip(direction)
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        game.run(event)
    pygame.quit()
