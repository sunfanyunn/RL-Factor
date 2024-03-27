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
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
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
        circle.rect.x = random.randrange(0, GRID_WIDTH) * GRID_SIZE
        circle.rect.y = random.randrange(0, GRID_HEIGHT) * GRID_SIZE
        while pygame.sprite.spritecollideany(circle, self.circles) or pygame.sprite.collide_rect(circle, self.agent):
            circle.rect.x = random.randrange(0, GRID_WIDTH) * GRID_SIZE
            circle.rect.y = random.randrange(0, GRID_HEIGHT) * GRID_SIZE
        self.circles.add(circle)

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        collided_circles = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collided_circles:
            if circle.color == GREEN:
                self.score += 1
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))
        self.circles.update()

    def reset_game(self):
        """
        Reset the game state.
        """
        self.game_over = False
        self.score = 0
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
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
        return True

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.circles.draw(self.screen)
        self.agent.update()
        self.agent.draw(self.screen)

        if not self.game_over:
            score_text = self.font.render(f'Score: {self.score}', True, BLUE)
            self.screen.blit(score_text, (10, 10))
        else:
            self.show_message('Game Over!')

        if all(circle.color == RED for circle in self.circles):
            self.game_over = True
            self.show_message('You won! Press R to Restart', 24)
        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        message_font = pygame.font.SysFont(None, size)
        message_surface = message_font.render(message, True, BLUE)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        """
        Main game loop.
        """
        if self.handle_events(event):
            if not self.game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.agent.move((0, -1))
                if keys[pygame.K_DOWN]:
                    self.agent.move((0, 1))
                if keys[pygame.K_LEFT]:
                    self.agent.move((-1, 0))
                if keys[pygame.K_RIGHT]:
                    self.agent.move((1, 0))
                self.update_circles()
            self.render_game()
            self.clock.tick(FPS)
            return True
        else:
            return False


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
        x_move, y_move = direction
        self.rect.x += x_move * GRID_SIZE
        self.rect.y += y_move * GRID_SIZE
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

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
        self.direction = random.choice([(1,0), (0,1), (-1,0), (0,-1)])
        self.move_smoothly()

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.x = random.randrange(0, GRID_WIDTH) * GRID_SIZE
        self.rect.y = random.randrange(0, GRID_HEIGHT) * GRID_SIZE
        self.direction = random.choice([(1,0), (0,1), (-1,0), (0,-1)])

    def update(self):
        """
        Update the circle's position.
        """
        self.move_smoothly()

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        x_move, y_move = self.direction
        self.rect.x += x_move * GRID_SIZE
        self.rect.y += y_move * GRID_SIZE
        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width or self.rect.y < 0 or self.rect.y > HEIGHT - self.rect.height:
            self.reset()


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

