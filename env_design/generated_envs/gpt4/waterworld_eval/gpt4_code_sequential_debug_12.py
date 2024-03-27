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
        self.all_sprites = pygame.sprite.Group(self.agent)
        self.font = pygame.font.Font(None, 36)
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(5):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        new_circle = Circle(color)
        new_circle.reset()
        while pygame.sprite.spritecollideany(new_circle, self.all_sprites):
            new_circle.reset()
        self.circles.add(new_circle)
        self.all_sprites.add(new_circle)

    def update_circles(self):
        for circle in list(self.circles):
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(random.choice([GREEN, RED]))
        if not any(c.color == GREEN for c in self.circles):
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.agent.reset()
        for circle in self.circles:
            circle.kill()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.agent.move('up')
            elif event.key == pygame.K_DOWN:
                self.agent.move('down')
            elif event.key == pygame.K_LEFT:
                self.agent.move('left')
            elif event.key == pygame.K_RIGHT:
                self.agent.move('right')

    def render_game(self):
        self.screen.fill(WHITE)
        score_text = self.font.render("Score: " + str(self.score), True, BLUE)
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message("Game Over!")
        else:
            self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_message(self, message, size=64):
        message_font = pygame.font.Font(None, size)
        message_surface = message_font.render(message, True, RED)
        x = (WIDTH - message_surface.get_width()) // 2
        y = (HEIGHT - message_surface.get_height()) // 2
        self.screen.blit(message_surface, (x, y))
        pygame.display.flip()

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
            self.agent.update()
            self.circles.update()
        self.render_game()
        self.clock.tick(FPS)
        return not self.game_over


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.radius = CIRCLE_RADIUS

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


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.radius = CIRCLE_RADIUS
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(self.radius, WIDTH - self.radius), random.randint(self.radius, HEIGHT - self.radius))

    def update(self):
        if random.random() < 0.1:
            self.move_smoothly()

    def move_smoothly(self):
        move = random.choice([(0, -GRID_SIZE), (0, GRID_SIZE), (-GRID_SIZE, 0), (GRID_SIZE, 0)])
        new_x = self.rect.x + move[0]
        new_y = self.rect.y + move[1]
        if 0 <= new_x <= WIDTH - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= HEIGHT - self.rect.height:
            self.rect.y = new_y

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
