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

        self.all_sprites = pygame.sprite.Group()
        self.agent = Agent()
        self.all_sprites.add(self.agent)

        self.green_circles = pygame.sprite.Group()
        self.red_circles = pygame.sprite.Group()
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(GRID_WIDTH * GRID_HEIGHT // 100):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        while True:
            pos_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            pos_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle = Circle(color)
            new_circle.rect.topleft = pos_x, pos_y
            if not pygame.sprite.spritecollide(new_circle, self.all_sprites, False):
                self.all_sprites.add(new_circle)
                if color == GREEN:
                    self.green_circles.add(new_circle)
                else:
                    self.red_circles.add(new_circle)
                break

    def update_circles(self):
        green_hit_list = pygame.sprite.spritecollide(self.agent, self.green_circles, True)
        red_hit_list = pygame.sprite.spritecollide(self.agent, self.red_circles, True)

        for _ in green_hit_list:
            self.score += 1
            self.spawn_circle(random.choice([GREEN, RED]))

        for _ in red_hit_list:
            self.score -= 1
            self.spawn_circle(random.choice([GREEN, RED]))

        for circle in list(self.green_circles) + list(self.red_circles):
            circle.move_smoothly()

        if not self.green_circles:
            self.game_over = True

    def reset_game(self):
        self.all_sprites.empty()
        self.green_circles.empty()
        self.red_circles.empty()
        self.score = 0
        self.game_over = False
        self.agent.reset()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RETURN:
                if self.game_over:
                    self.reset_game()
            elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.agent.move(DIRS[event.key])

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            self.show_message('Game Over! Press Enter to play again.')

        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        message_surf = font.render(message, True, BLUE)
        message_rect = message_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message_surf, message_rect)

    def run(self, event):
        self.clock.tick(FPS)
        self.handle_events(event)

        if not self.game_over:
            self.update_circles()

        self.render_game()
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
        self.rect.x += direction[0]
        self.rect.y += direction[1]
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
        self.color = color
        pygame.draw.circle(self.image, color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS)
        self.rect = self.image.get_rect()
        dir_choices = [-1, 0, 1]
        self.vx = random.choice(dir_choices) * GRID_SIZE // 4
        self.vy = random.choice(dir_choices) * GRID_SIZE // 4

    def move_smoothly(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy = -self.vy


DIRS = {
    pygame.K_UP:    (0, -GRID_SIZE),
    pygame.K_DOWN:  (0, GRID_SIZE),
    pygame.K_LEFT:  (-GRID_SIZE, 0),
    pygame.K_RIGHT: (GRID_SIZE, 0)
}

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
