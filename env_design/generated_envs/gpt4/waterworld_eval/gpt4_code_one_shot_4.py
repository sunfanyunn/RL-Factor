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
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.score = 0
        self.green_count = 0
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        count = GRID_WIDTH * GRID_HEIGHT // 40  # Adjust initial circle numbers based on the grid size.
        for _ in range(count):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)
            self.green_count += 1

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
        for circle in pygame.sprite.spritecollide(self.agent, self.circles, dokill=True):
            if circle.color == GREEN:
                self.score += 1
                self.green_count -= 1
            else:
                self.score -= 1
            # Respawn as green or red with 50/50 chance
            new_color = GREEN if random.choice([True, False]) else RED
            if new_color == GREEN:
                self.green_count += 1
            self.spawn_circle(new_color)

    def reset_game(self):
        """
        Reset the game state.
        """
        self.score = 0
        self.game_over = False
        self.agent.reset()
        self.circles.empty()
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
        # Display score
        score_text = self.font.render(f"Score: {self.score}", True, BLUE)
        self.screen.blit(score_text, (10, 10))

        # Draw all circles
        self.circles.draw(self.screen)

        # Draw the agent
        self.agent.draw(self.screen)

        if self.game_over:
            self.show_message("Game Over!")

        pygame.display.flip()

    def show_message(self, message, size=36):
        """
        Display a message on the screen.
        """
        message_surface = self.font.render(message, True, BLUE)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.fill(WHITE)
        self.screen.blit(message_surface, message_rect)
        pygame.display.flip()
          
    def run(self, event):
        """
        Main game loop.
        """
        if not self.game_over:
            self.handle_events(event)
            self.agent.update()
            self.update_circles()
            self.render_game()
            if self.green_count <= 0:
                self.game_over = True
                self.show_message("You won! Press 'R' to restart.")
            self.clock.tick(FPS)
        return self.handle_events(event)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            running = game.run(event)
        game.clock.tick(FPS)
    pygame.quit()
