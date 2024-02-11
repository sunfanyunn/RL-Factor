import pygame
import sys

WIDTH, HEIGHT = 640, 480
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.topleft = (WIDTH // 2, HEIGHT // 2)
        self.speed = [5, 5]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]

    def bounce(self):
        self.speed[0] = -self.speed[0]


class PaddleHuman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.reset()
        self.speed = 10

    def reset(self):
        self.rect.topleft = (10, HEIGHT // 2 - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


class PaddleCPU(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.reset()
        self.speed = 5

    def reset(self):
        self.rect.topleft = (WIDTH - 30, HEIGHT // 2 - 50)

    def update(self):
        # Simple CPU control, follows the ball
        if self.rect.centery < game.ball.rect.centery and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        elif self.rect.centery > game.ball.rect.centery and self.rect.top > 0:
            self.rect.y -= self.speed


class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Game")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.all_sprites = pygame.sprite.Group()
        self.ball = Ball()
        self.paddle_human = PaddleHuman()
        self.paddle_cpu = PaddleCPU()
        self.all_sprites.add(self.ball, self.paddle_human, self.paddle_cpu)

        self.score_human = 0
        self.score_cpu = 0
        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()

    def render_game(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # Display scores
        score_text = self.font.render(
            f"{self.score_human} - {self.score_cpu}", True, WHITE
        )
        score_rect = score_text.get_rect(center=(WIDTH // 2, 20))
        self.screen.blit(score_text, score_rect)

        if self.game_over:
            self.show_message("Game Over. Press 'R' to restart.", 36, HEIGHT // 2)
        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self, event):
        if not self.game_over:
            self.all_sprites.update()

            if self.ball.rect.colliderect(
                self.paddle_human.rect
            ) or self.ball.rect.colliderect(self.paddle_cpu.rect):
                self.ball.bounce()

            if self.ball.rect.left < 0:
                self.score_cpu += 1
                self.reset_round()
            elif self.ball.rect.right > WIDTH:
                self.score_human += 1
                self.reset_round()

            if self.ball.rect.left < 0 or self.ball.rect.right > WIDTH:
                self.game_over = True

        self.render_game()

    def reset_round(self):
        self.ball.reset()
        self.paddle_human.reset()
        self.paddle_cpu.reset()

    def reset_game(self):
        self.score_human = 0
        self.score_cpu = 0
        self.game_over = False
        self.reset_round()


if __name__ == "__main__":
    game = PongGame()
    game.run()
