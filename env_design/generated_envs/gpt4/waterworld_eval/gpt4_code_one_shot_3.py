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
        self.font = pygame.font.SysFont('Arial', 24)
        self.agent = Agent()
        self.agent_group = pygame.sprite.GroupSingle(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(10): # Assuming we want 10 of each for a start
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            circle = Circle(color)
            circle.rect.topleft = pos
            if not any(spr.rect.colliderect(circle.rect) for spr in self.circles):
                self.circles.add(circle)
                break

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                self.score += 1 if circle.color == GREEN else -1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([GREEN, RED]))
            else:
                circle.move_smoothly()
        green_circles = sum(1 for circle in self.circles if circle.color == GREEN)
        if green_circles == 0:
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
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            elif event.key == pygame.K_UP:
                self.agent.move('up')
            elif event.key == pygame.K_DOWN:
                self.agent.move('down')
            elif event.key == pygame.K_LEFT:
                self.agent.move('left')
            elif event.key == pygame.K_RIGHT:
                self.agent.move('right')
        return True

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        score_text = self.font.render(f'Score: {self.score}', True, GREEN)
        self.screen.blit(score_text, (5, 5))

        if self.game_over:
            self.show_message("Game Over!")

        self.agent_group.draw(self.screen)
        self.circles.draw(self.screen)
        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont('Arial', size)
        text_surface = font.render(message, True, RED)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def run(self, event):
        """
        Main game loop.
        """
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
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
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def reset(self):
        """
        Reset the agent's position.
        """
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, direction):
        """
        Move the agent in the specified direction.
        """
        movements = {'up': (0, -GRID_SIZE), 'down': (0, GRID_SIZE), 'left': (-GRID_SIZE, 0), 'right': (GRID_SIZE, 0)}
        if direction in movements:
            move_x, move_y = movements[direction]
            self.rect.move_ip(move_x, move_y)
            self.rect.clamp_ip(self.screen.get_rect())

    def update(self):
        """
        Update method for the agent (unused in this example).
        """
        pass


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
        pygame.draw.circle(
            self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()
        self.velocity = [random.choice([-1, 1]) * GRID_SIZE,
                         random.choice([-1, 1]) * GRID_SIZE]

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.topleft = (random.randint(0, GRID_WIDTH) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT) * GRID_SIZE)
        self.velocity = [random.choice([-1, 1]) * GRID_SIZE,
                         random.choice([-1, 1]) * GRID_SIZE]

    def update(self):
        """
        Update the circle's position.
        """
        pass

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        self.rect.move_ip(self.velocity)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.velocity[1] = -self.velocity[1]

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

