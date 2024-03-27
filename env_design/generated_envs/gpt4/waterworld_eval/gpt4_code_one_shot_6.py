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

        # Creating sprite groups
        self.agent = Agent()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.circles = pygame.sprite.Group()

        # Spawn initial circles
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(10):  # Spawn a total of 20 circles, 10 green, and 10 red.
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        circle_created = False
        while not circle_created:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle = Circle(color)
            new_circle.rect.topleft = (x, y)
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                self.all_sprites.add(new_circle)
                circle_created = True

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
                # Respawn the circle as either a red or green circle randomly
                self.spawn_circle(random.choice([RED, GREEN]))

        # Check for game over condition
        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.score = 0
        self.game_over = False
        self.circles.empty()
        self.all_sprites.empty()
        self.agent.reset()
        self.all_sprites.add(self.agent)
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
        self.all_sprites.draw(self.screen)

        score_text = self.font.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(score_text, (5, 5))

        if self.game_over:
            self.show_message('Game Over! Press R to Restart', size=48)

        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont(None, size)
        message_surface = font.render(message, True, BLACK)
        xpos = (WIDTH - message_surface.get_width()) // 2
        ypos = (HEIGHT - message_surface.get_height()) // 2
        self.screen.blit(message_surface, (xpos, ypos))

    def run(self, event):
        """
        Main game loop.
        """
        if not self.handle_events(event):
            return False

        if not self.game_over:
            self.agent.update()
            self.update_circles()
            self.circles.update()

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
        if direction == 'up' and self.rect.y > 0:
            self.rect.y -= GRID_SIZE
        elif direction == 'down' and self.rect.y < HEIGHT - (CIRCLE_RADIUS * 2):
            self.rect.y += GRID_SIZE
        elif direction == 'left' and self.rect.x > 0:
            self.rect.x -= GRID_SIZE
        elif direction == 'right' and self.rect.x < WIDTH - (CIRCLE_RADIUS * 2):
            self.rect.x += GRID_SIZE


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
        self.reset()

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, 
                            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def update(self):
        """
        Update the circle's position.
        """
        self.move_smoothly()


    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        new_x = self.rect.x + self.direction[0]
        new_y = self.rect.y + self.direction[1]
        # Wrap around the screen edges
        if new_x < 0:
            new_x = WIDTH - CIRCLE_RADIUS * 2
        elif new_x > WIDTH - CIRCLE_RADIUS * 2:
            new_x = 0
        if new_y < 0:
            new_y = HEIGHT - CIRCLE_RADIUS * 2
        elif new_y > HEIGHT - CIRCLE_RADIUS * 2:
            new_y = 0
        self.rect.x = new_x
        self.rect.y = new_y


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.agent.move('up')
            elif event.key == pygame.K_DOWN:
                game.agent.move('down')
            elif event.key == pygame.K_LEFT:
                game.agent.move('left')
            elif event.key == pygame.K_RIGHT:
                game.agent.move('right')
        running = game.run(event)
    pygame.quit()

