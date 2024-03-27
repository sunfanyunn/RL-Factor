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
        self.font = pygame.font.Font(None, 36)
        
        self.agent = Agent()
        self.agent.screen = self.screen
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.circles = pygame.sprite.Group()
        self.spawn_initial_circles()
    
    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)
    
    def spawn_circle(self, color):
        new_circle = Circle(color)
        new_circle.screen = self.screen
        circle_created = False
        while not circle_created:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle.rect.topleft = (x, y)
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                self.all_sprites.add(new_circle)
                circle_created = True

    def update_circles(self):
        for circle in list(self.circles):
            circle.move_smoothly()
            if pygame.sprite.collide_circle(self.agent, circle):
                if circle.color == GREEN:
                    self.score += 1
                else:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(random.choice([RED, GREEN]))
        self.check_game_over()
    
    def check_game_over(self):
        if not any(circle.color == GREEN for circle in self.circles):
            self.game_over = True

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.agent.reset()
        for circle in self.circles:
            circle.kill()
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            else:
                self.agent.move(event.key)

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message('Game Over! Press R to Restart', size=48)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        msg_surface = font.render(message, True, RED)
        msg_rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(msg_surface, msg_rect)

    def run(self, event):
        if not self.game_over:
            self.handle_events(event)
            self.all_sprites.update()
            self.update_circles()
        self.render_game()
        self.clock.tick(FPS)


class Agent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, key):
        if key == pygame.K_UP:
            self.rect.y -= GRID_SIZE
        elif key == pygame.K_DOWN:
            self.rect.y += GRID_SIZE
        elif key == pygame.K_LEFT:
            self.rect.x -= GRID_SIZE
        elif key == pygame.K_RIGHT:
            self.rect.x += GRID_SIZE
        self.rect.clamp_ip(self.screen.get_rect())


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        self.vx = random.choice([-1, 1])
        self.vy = random.choice([-1, 1])

    def move_smoothly(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx = -self.vx
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy

if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.run(event)
    pygame.quit()

