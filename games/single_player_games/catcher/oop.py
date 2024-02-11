import pygame
import random

WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE * 4, GRID_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((WIDTH - self.rect.width) // 2, HEIGHT - GRID_SIZE)

    def reset(self):
        self.rect.topleft = ((WIDTH - self.rect.width) // 2, HEIGHT - GRID_SIZE)

    def move_left(self):
        self.rect.x -= GRID_SIZE * 2
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += GRID_SIZE * 2
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, 0)

    def update(self):
        self.rect.y += GRID_SIZE / 4


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.game_over = False

        self.catcher = Catcher()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.catcher)

        self.balls = []
        self.balls.append(Ball())
        self.all_sprites.add(self.balls[0])

    def render_game(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        if self.game_over:
            size = 36
            message = "Game Over. Click to play again."
            font = pygame.font.Font(None, size)
            text = font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
        else:
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self, event):
        if event.type == pygame.QUIT:
            return False

        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.reset_game()
            return True
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.catcher.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.catcher.move_right()

            self.catcher.update()
            for ball in self.balls:
                ball.update()

                # Check if the catcher caught the ball
                if pygame.sprite.collide_rect(self.catcher, ball):
                    self.reset_ball()
                    self.score += 1

                # Check if the ball reached the bottom
                if ball and ball.rect.bottom >= HEIGHT:
                    self.game_over = True

        self.render_game()
        return True

    def reset_ball(self):
        self.balls[0].kill()
        self.balls = []
        self.ball = Ball()
        self.balls.append(self.ball)
        self.all_sprites.add(self.ball)


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()