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
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.green_circle_count = 3
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(self.green_circle_count):
            self.spawn_circle(GREEN)
        for _ in range(self.green_circle_count):
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        while True:
            new_circle = Circle(color, self)
            new_circle.reset()
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                break

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(circle, self.agent):
                if circle.color == GREEN:
                    self.score += 1
                    self.green_circle_count -= 1
                else:
                    self.score -= 1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([GREEN, RED]))
                if self.green_circle_count <= 0:
                    self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.game_over = False
        self.score = 0
        self.circles.empty()
        self.agent.reset()
        self.green_circle_count = 3
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            elif not self.game_over:
                self.agent.move_event(event)

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        for sprite in self.circles:
            sprite.update()
        self.agent.update()
        self.circles.draw(self.screen)
        self.screen.blit(self.agent.image, self.agent.rect)
        self.show_message('Score: ' + str(self.score), 24, (30, 10), BLUE)

        if self.game_over:
            self.show_message('Game Over! Press R to restart', 36, (WIDTH // 2, HEIGHT // 2), RED)

    def show_message(self, message, size=36, position=None, color=BLUE):
        """
        Display a message on the screen.
        """
        if position is None:
            position = (WIDTH // 2, HEIGHT // 2)
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.screen.blit(text_surface, text_rect)

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
        super().__init__()
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move_event(self, event):
        if event.key == pygame.K_LEFT:
            self.move((-1, 0))
        elif event.key == pygame.K_RIGHT:
            self.move((1, 0))
        elif event.key == pygame.K_UP:
            self.move((0, -1))
        elif event.key == pygame.K_DOWN:
            self.move((0, 1))

    def move(self, direction):
        move_x, move_y = direction
        self.rect.centerx = (self.rect.centerx + (move_x * GRID_SIZE)) % WIDTH
        self.rect.centery = (self.rect.centery + (move_y * GRID_SIZE)) % HEIGHT


class Circle(pygame.sprite.Sprite):
    def __init__(self, color, game):
        super().__init__()
        self.color = color
        self.game = game
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()

    def reset(self):
        self.rect.topleft = (random.randrange(WIDTH - CIRCLE_RADIUS * 2), random.randrange(HEIGHT - CIRCLE_RADIUS * 2))

    def update(self):
        if not self.game.game_over:
            self.move_smoothly()

    def move_smoothly(self):
        move_x, move_y = random.choice([(0, -2), (0, 2), (-2, 0), (2, 0)])
        self.rect.x = (self.rect.x + move_x) % WIDTH
        self.rect.y = (self.rect.y + move_y) % HEIGHT

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.run(event)
        pygame.display.flip()
    pygame.quit()

