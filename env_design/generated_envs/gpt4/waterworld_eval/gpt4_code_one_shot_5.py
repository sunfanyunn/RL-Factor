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
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

        self.font = pygame.font.SysFont('arial', 24)

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(GRID_WIDTH * GRID_HEIGHT // (4 * CIRCLE_RADIUS)):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        while True:
            location = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            new_circle = Circle(color)
            new_circle.rect.topleft = location
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                self.all_sprites.add(new_circle)
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
                else:
                    self.score -= 1
                self.circles.remove(circle)
                self.all_sprites.remove(circle)
                self.spawn_circle(random.choice([RED, GREEN]))

        green_circles = [circle for circle in self.circles if circle.color == GREEN]
        if not green_circles:
            self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.score = 0
        self.game_over = False
        self.agent.reset()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.agent.move((0, -GRID_SIZE))
            elif event.key == pygame.K_DOWN:
                self.agent.move((0, GRID_SIZE))
            elif event.key == pygame.K_LEFT:
                self.agent.move((-GRID_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                self.agent.move((GRID_SIZE, 0))
            elif event.key == pygame.K_r and self.game_over:
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            self.show_message('Game Over! Press R to Restart', 48)

        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont('arial', size)
        message_surface = font.render(message, True, RED)
        message_rect = message_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        """
        Main game loop.
        """
        self.handle_events(event)
        if not self.game_over:
            self.all_sprites.update()
            self.update_circles()
        self.render_game()
        self.clock.tick(FPS)
        return True


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
        self.rect.x += direction[0]
        self.rect.y += direction[1]
       
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
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def update(self):
        """
        Update the circle's position.
        """
        new_position = self.rect.move(self.direction[0] * GRID_SIZE, self.direction[1] * GRID_SIZE)
        if 0 <= new_position.x < WIDTH and 0 <= new_position.y < HEIGHT:
            self.rect = new_position
        else:
            self.direction = random.choice([(1,0), (0,1), (-1,0), (0,-1)])

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        self.direction = random.choice([(1,0), (0,1), (-1,0), (0,-1)])


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

