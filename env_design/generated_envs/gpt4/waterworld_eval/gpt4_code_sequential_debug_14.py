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
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WaterWorld Game")
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.agent = Agent()
        self.circles = pygame.sprite.Group()
        self.agent_sprite = pygame.sprite.GroupSingle(self.agent)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        circle = Circle(color)
        while pygame.sprite.spritecollideany(circle, self.circles):
            circle.reset()
        self.circles.add(circle)

    def update_circles(self):
        for circle in list(self.circles):
            if circle.rect.colliderect(self.agent.rect):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                self.circles.remove(circle)
                self.spawn_circle(random.choice([RED, GREEN]))
        green_circles = [circle for circle in self.circles if circle.color == GREEN]
        if not green_circles:
            self.game_over = True

    def reset_game(self):
        self.score = 0
        self.agent.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
            elif not self.game_over:
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        for circle in self.circles:
            circle.update()
        self.circles.draw(self.screen)
        self.agent_sprite.draw(self.screen)
        font = pygame.font.SysFont(None, 36)
        score_text = font.render('Score: ' + str(self.score), True, BLUE)
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message('Game Over! Press R to restart', 48)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont('arial', size)
        message_surface = font.render(message, True, RED)
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)

    def run(self, event):
        self.clock.tick(FPS)
        if event:
            self.handle_events(event)
        if not self.game_over:
            self.update_circles()
        self.render_game()
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (GRID_SIZE // 2, GRID_SIZE // 2), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, direction):
        if direction == pygame.K_UP and self.rect.top > 0:
            self.rect.y -= GRID_SIZE
        elif direction == pygame.K_DOWN and self.rect.bottom < HEIGHT:
            self.rect.y += GRID_SIZE
        elif direction == pygame.K_LEFT and self.rect.left > 0:
            self.rect.x -= GRID_SIZE
        elif direction == pygame.K_RIGHT and self.rect.right < WIDTH:
            self.rect.x += GRID_SIZE


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (GRID_SIZE // 2, GRID_SIZE // 2), CIRCLE_RADIUS)
        self.reset()
    
    def reset(self):
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
    
    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        direction = random.choice([(0, -GRID_SIZE), (0, GRID_SIZE), (-GRID_SIZE, 0), (GRID_SIZE, 0)])
        self.rect.x += direction[0]
        self.rect.y += direction[1]
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).contains(self.rect):
            self.reset()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            running = game.run(event)
        if not running:
            break
    pygame.quit()

