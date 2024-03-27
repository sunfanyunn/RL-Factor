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

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.green_circles = pygame.sprite.Group()
        self.red_circles = pygame.sprite.Group()

        self.agent = Agent()
        self.all_sprites.add(self.agent)

        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        for _ in range(GRID_WIDTH * GRID_HEIGHT // 2):
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
            if not pygame.sprite.spritecollide(circle, self.all_sprites, False):
                self.all_sprites.add(circle)
                if color == GREEN:
                    self.green_circles.add(circle)
                elif color == RED:
                    self.red_circles.add(circle)
                break

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        green_hit_list = pygame.sprite.spritecollide(self.agent, self.green_circles, True)
        red_hit_list = pygame.sprite.spritecollide(self.agent, self.red_circles, True)

        for hit in green_hit_list:
            self.score += 1
            self.spawn_circle(random.choice([GREEN, RED]))

        for hit in red_hit_list:
            self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))

        if not self.green_circles:
            self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.game_over = False
        self.score = 0
        self.all_sprites.empty()
        self.green_circles.empty()
        self.red_circles.empty()
        self.agent.reset()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_RETURN:
                if self.game_over:
                    self.reset_game()
            elif event.key == pygame.K_UP:
                self.agent.move((0, -GRID_SIZE))
            elif event.key == pygame.K_DOWN:
                self.agent.move((0, GRID_SIZE))
            elif event.key == pygame.K_LEFT:
                self.agent.move((-GRID_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                self.agent.move((GRID_SIZE, 0))

        return True

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render('Score: {}'.format(self.score), True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            self.show_message('Game Over! Press Enter to play again.')

        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont(None, size)
        message_surf = font.render(message, True, BLUE)
        message_rect = message_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surf, message_rect)

    def run(self, event):
        """
        Main game loop.
        """
        if not self.handle_events(event):
            return False

        if not self.game_over:
            self.update_circles()
            self.all_sprites.update()

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
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

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
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_smoothly()


    def reset(self):
        """
        Reset the circle's position and direction.
        """
        self.rect.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def update(self):
        """
        Update the circle's position.
        """
        self.rect.x += self.direction[0] * 2  # Adjust speed if necessary
        self.rect.y += self.direction[1] * 2
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])

        self.move_smoothly()

    def move_smoothly(self):
        """
        Move the circle smoothly across the screen.
        """
        self.rect.x += self.direction[0] * random.uniform(0.5, 1.5) * 2
        self.rect.y += self.direction[1] * random.uniform(0.5, 1.5) * 2


if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
