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
        self.font = pygame.font.SysFont('Arial', 25)

        self.agent = Agent()
        self.all_sprites = pygame.sprite.Group()
        self.circles = pygame.sprite.Group()
        self.all_sprites.add(self.agent)
        self.green_count = 0

        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        for _ in range(10):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        new_circle = Circle(color)
        while True:
            new_circle.rect.topleft = (random.randrange(GRID_WIDTH) * GRID_SIZE, random.randrange(GRID_HEIGHT) * GRID_SIZE)
            if pygame.sprite.spritecollideany(new_circle, self.circles) is None:
                break
        self.circles.add(new_circle)
        self.all_sprites.add(new_circle)
        if color == GREEN:
            self.green_count += 1

    def update_circles(self):
        for circle in self.circles:
            if self.agent.rect.colliderect(circle.rect):
                if circle.color == GREEN:
                    self.score += 1
                    self.green_count -= 1
                else:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(random.choice([GREEN, RED]))

    def reset_game(self):
        self.all_sprites.empty()
        self.circles.empty()
        self.score = 0
        self.game_over = False
        self.green_count = 0
        self.agent.reset()
        self.all_sprites.add(self.agent)
        self.spawn_initial_circles()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.agent.move(event.key)
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def render_game(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        score_text = self.font.render('Score: ' + str(self.score), True, BLACK)
        self.screen.blit(score_text, (5, 5))
        if self.game_over:
            self.show_message("Game Over!", 50)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.SysFont('Arial', size)
        message = font.render(message, True, BLACK)
        message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message, message_rect)

    def run(self, event):
        self.handle_events(event)
        if not self.game_over:
            self.update_circles()
            self.render_game()
            if self.green_count == 0:
                self.game_over = True
        self.clock.tick(FPS)
        return True


class Agent(pygame.sprite.Sprite):
    def __init__(self):
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

        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

    def update(self):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface(
            (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.rect = self.image.get_rect()
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.rect.topleft = (random.randrange(GRID_WIDTH) * GRID_SIZE, random.randrange(GRID_HEIGHT) * GRID_SIZE)

    def reset(self):
        self.rect.topleft = (random.randrange(GRID_WIDTH) * GRID_SIZE, random.randrange(GRID_HEIGHT) * GRID_SIZE)
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        new_pos = (self.rect.x + self.direction[0] * 5, self.rect.y + self.direction[1] * 5)
        self.rect.x, self.rect.y = new_pos

        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.direction = (-self.direction[0], self.direction[1])
        if self.rect.y < 0 or self.rect.y > HEIGHT - self.rect.height:
            self.direction = (self.direction[0], -self.direction[1])

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
