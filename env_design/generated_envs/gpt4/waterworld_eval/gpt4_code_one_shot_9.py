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
        self.all_sprites = pygame.sprite.Group()
        self.agent = Agent()
        self.all_sprites.add(self.agent)
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
        while True:
            pos_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            pos_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            circle = Circle(color)
            circle.rect.topleft = (pos_x, pos_y)
            if not pygame.sprite.spritecollideany(circle, self.all_sprites):
                self.circles.add(circle)
                self.all_sprites.add(circle)
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
                circle.kill()
                self.spawn_circle(random.choice([GREEN, RED]))
                if len([s for s in self.circles if s.color == GREEN]) == 0:
                    self.game_over = True

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
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(text, (5, 5))
        self.all_sprites.draw(self.screen)
        if self.game_over:
            self.show_message('Game Over! Press R to Restart')
        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont(None, size)
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

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
        if direction == 'UP' and self.rect.top > 0:
            self.rect.move_ip(0, -GRID_SIZE)
        elif direction == 'DOWN' and self.rect.bottom < HEIGHT:
            self.rect.move_ip(0, GRID_SIZE)
        elif direction == 'LEFT' and self.rect.left > 0:
            self.rect.move_ip(-GRID_SIZE, 0)
        elif direction == 'RIGHT' and self.rect.right < WIDTH:
            self.rect.move_ip(GRID_SIZE, 0)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move('UP')
        elif keys[pygame.K_DOWN]:
            self.move('DOWN')
        elif keys[pygame.K_LEFT]:
            self.move('LEFT')
        elif keys[pygame.K_RIGHT]:
            self.move('RIGHT')


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
        self.move_smoothly()

    def reset(self):
        """
        Reset the circle's position and direction.
        """
        pos_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        pos_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.rect.topleft = (pos_x, pos_y)

    def update(self):
        """
        Update the circle's position.
        """
        self.move_smoothly()

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        directions = [(0, GRID_SIZE), (0, -GRID_SIZE), (GRID_SIZE, 0), (-GRID_SIZE, 0)]
        direction = random.choice(directions)
        self.rect.move_ip(*direction)
        if not (0 <= self.rect.top <= HEIGHT - CIRCLE_RADIUS * 2):
            self.rect.top = max(0, min(self.rect.top, HEIGHT - CIRCLE_RADIUS * 2))
        if not (0 <= self.rect.left <= WIDTH - CIRCLE_RADIUS * 2):
            self.rect.left = max(0, min(self.rect.left, WIDTH - CIRCLE_RADIUS * 2))

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

