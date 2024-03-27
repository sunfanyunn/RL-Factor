import pygame
import sys
import random

# Game constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60
CIRCLE_RADIUS = 10

# Color definitions
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Circle Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.agent = Agent()
        self.agent_sprite_group = pygame.sprite.Group(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        self.circles.add(circle)

    def update_circles(self):
        for circle in list(self.circles):
            if self.agent.rect.colliderect(circle.rect):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                self.spawn_circle(random.choice([GREEN, RED]))
                self.circles.remove(circle)

        green_circles = [circle for circle in self.circles if circle.color == GREEN]
        if not green_circles:
            self.game_over = True

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.circles.empty()
        self.agent.reset()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.agent.move('up')
            elif event.key == pygame.K_DOWN:
                self.agent.move('down')
            elif event.key == pygame.K_LEFT:
                self.agent.move('left')
            elif event.key == pygame.K_RIGHT:
                self.agent.move('right')
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def render_game(self):
        self.screen.fill(WHITE)
        if self.game_over:
            self.show_message("Game Over! Score: " + str(self.score), size=48)
        else:
            score_text = self.font.render("Score: " + str(self.score), True, BLUE)
            self.screen.blit(score_text, (10, 10))
            self.circles.draw(self.screen)
            self.agent_sprite_group.draw(self.screen)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont(None, size)
        text = font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(text, text_rect)

    def run(self, event):
        if not self.game_over:
            self.clock.tick(FPS)
            self.handle_events(event)
            self.update_circles()
            self.agent_sprite_group.update()
            self.circles.update()
            self.render_game()
        else:
            self.show_message("Press any key to restart", size=36)
            pygame.display.flip()
            if event.type == pygame.KEYUP:
                self.reset_game()

        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        if direction == 'up' and self.rect.top > 0:
            self.rect.y -= GRID_SIZE
        elif direction == 'down' and self.rect.bottom < HEIGHT:
            self.rect.y += GRID_SIZE
        elif direction == 'left' and self.rect.left > 0:
            self.rect.x -= GRID_SIZE
        elif direction == 'right' and self.rect.right < WIDTH:
            self.rect.x += GRID_SIZE

    def update(self):
        pass

class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.color = random.choice([RED, GREEN]) # Respawn as red or green circle
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)

    def update(self):
        # Stop circle movement when the game is over
        if game.game_over:
            return
        move_x = random.choice([-GRID_SIZE, GRID_SIZE])
        move_y = random.choice([-GRID_SIZE, GRID_SIZE])
        self.rect.move_ip(move_x, move_y)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x -= move_x
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.rect.y -= move_y

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = game.run(event)
    pygame.quit()
