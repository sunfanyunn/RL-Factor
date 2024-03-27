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
        self.all_sprites = pygame.sprite.Group()
        self.circles = pygame.sprite.Group()
        self.agent = Agent()
        self.all_sprites.add(self.agent)
        self.colors = [RED, GREEN]
        self.green_count = 10
        for _ in range(self.green_count * 2):
            self.spawn_initial_circles()

    def spawn_initial_circles(self):
        """
        Spawn initial circles on the game grid.
        """
        color = self.colors.pop(0)
        self.colors.append(color)
        new_circle = Circle(color)
        collision = True
        while collision:
            new_circle.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            collision = pygame.sprite.spritecollideany(new_circle, self.circles)
        self.circles.add(new_circle)
        self.all_sprites.add(new_circle)

    def spawn_circle(self, color):
        """
        Spawn a circle with the given color on the game grid.
        Ensure no collision with existing sprites.
        """
        new_circle = Circle(color)
        collision = True
        while collision:
            new_circle.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            collision = pygame.sprite.spritecollideany(new_circle, self.circles)
        self.circles.add(new_circle)
        self.all_sprites.add(new_circle)

    def update_circles(self):
        """
        Update circles based on collisions with the agent.
        Update score accordingly.
        """
        for circle in self.circles:
            circle.move_smoothly()
        collided_circles = pygame.sprite.spritecollide(self.agent, self.circles, True)
        for circle in collided_circles:
            if circle.color == GREEN:
                self.score += 1
                self.green_count -= 1
            else:
                self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))
            if self.green_count <= 0:
                self.game_over = True

    def reset_game(self):
        """
        Reset the game state.
        """
        self.all_sprites.empty()
        self.circles.empty()
        self.agent.reset()
        self.all_sprites.add(self.agent)
        self.game_over = False
        self.score = 0
        self.colors = [RED, GREEN]
        self.green_count = 10
        for _ in range(self.green_count * 2):
            self.spawn_initial_circles()

    def handle_events(self, event):
        """
        Handle game events, including quitting and restarting the game.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.agent.move(event.key)
            elif event.key == pygame.K_r and self.game_over:
                self.reset_game()
        elif event.type == pygame.QUIT:
            return False
        return True

    def render_game(self):
        """
        Render the game screen, including sprites and score.
        Display game over or win messages as needed.
        """
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.show_message('Score: ' + str(self.score), 20, position=(5, 5))
        if self.game_over:
            self.show_message('Game Over!', 60, center=True)
        pygame.display.flip()

    def show_message(self, message, size=30, position=None, center=False):
        """
        Display a message on the screen.
        """
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
        else:
            text_rect.topleft = position
        self.screen.blit(text_surface, text_rect)

    def run(self, event):
        """
        Main game loop.
        """
        if not self.handle_events(event):
            return False
        if not self.game_over:
            self.update_circles()
            self.render_game()
        else:
            self.render_game()
        self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def reset(self):
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def move(self, direction):
        if direction == pygame.K_UP:
            self.rect.y -= GRID_SIZE
        elif direction == pygame.K_DOWN:
            self.rect.y += GRID_SIZE
        elif direction == pygame.K_LEFT:
            self.rect.x -= GRID_SIZE
        elif direction == pygame.K_RIGHT:
            self.rect.x += GRID_SIZE
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        if self.direction == pygame.K_UP:
            self.rect.y -= GRID_SIZE
        elif self.direction == pygame.K_DOWN:
            self.rect.y += GRID_SIZE
        elif self.direction == pygame.K_LEFT:
            self.rect.x -= GRID_SIZE
        elif self.direction == pygame.K_RIGHT:
            self.rect.x += GRID_SIZE

        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.reset()

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()

