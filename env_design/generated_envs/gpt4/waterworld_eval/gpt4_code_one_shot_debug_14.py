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
        self.circles = pygame.sprite.Group()
        self.agent = pygame.sprite.GroupSingle(Agent())
        self.spawn_initial_circles()

    def spawn_initial_circles(self):
        total_circles = 5
        self.green_circles = total_circles
        for _ in range(total_circles):
            self.spawn_circle(GREEN)
            self.spawn_circle(RED)

    def spawn_circle(self, color):
        valid_position = False
        while not valid_position:
            pos_x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            pos_y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_circle = Circle(color)
            new_circle.rect.topleft = (pos_x, pos_y)
            if not pygame.sprite.spritecollideany(new_circle, self.circles):
                self.circles.add(new_circle)
                valid_position = True

    def update_circles(self):
        for circle in self.circles:
            if pygame.sprite.collide_circle(circle, self.agent.sprite):
                if circle.color == GREEN:
                    self.score += 1
                    self.green_circles -= 1
                else:
                    self.score -= 1
                circle.kill()
                self.spawn_circle(random.choice([GREEN, RED]))
        if self.green_circles <= 0:
            self.game_over = True

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.green_circles = 0
        self.agent.sprite.reset()
        self.circles.empty()
        self.spawn_initial_circles()

    def handle_events(self, event):
        running = True
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
        return running

    def render_game(self):
        self.screen.fill(WHITE)
        self.agent.draw(self.screen)
        self.circles.draw(self.screen)
        self.show_score()
        if self.game_over:
            self.show_message("Game Over!", size=48)
        pygame.display.flip()

    def show_message(self, message, size=36):
        font = pygame.font.Font(None, size)
        text = font.render(message, True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def show_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: {}".format(self.score), True, BLUE)
        self.screen.blit(score_text, (5, 5))

    def run(self, event):
        self.clock.tick(FPS)
        if not self.game_over:
            self.agent.sprite.move(pygame.key.get_pressed())
        self.agent.update()
        self.circles.update()
        self.update_circles()
        self.render_game()
        return self.handle_events(event)


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
        x, y = self.rect.topleft
        if direction[pygame.K_UP]:
            y -= GRID_SIZE
        if direction[pygame.K_DOWN]:
            y += GRID_SIZE
        if direction[pygame.K_LEFT]:
            x -= GRID_SIZE
        if direction[pygame.K_RIGHT]:
            x += GRID_SIZE

        x = max(0, min(x, WIDTH - self.rect.width))
        y = max(0, min(y, HEIGHT - self.rect.height))
        self.rect.topleft = (x, y)

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
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_smoothly()

    def reset(self):
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.color = random.choice([GREEN, RED])
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(
            self.image, self.color, (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS
        )
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def update(self):
        self.move_smoothly()

    def move_smoothly(self):
        x, y = self.rect.topleft
        dir_x, dir_y = self.direction
        x += dir_x
        y += dir_y
        if x < 0 or x >= WIDTH - self.rect.width:
            dir_x *= -1
        if y < 0 or y >= HEIGHT - self.rect.height:
            dir_y *= -1
        self.direction = (dir_x, dir_y)
        self.rect.topleft = (x, y)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            running = game.run(event)
    pygame.quit()
