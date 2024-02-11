import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BALL_RADIUS = 15
BALL_SPEED = [3, 3]
PADDLE_SPEED = 5
PADDLE_DIMS = [10, 60]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, up_key, down_key):
        super().__init__()
        self.image = pygame.Surface(PADDLE_DIMS)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up_key]:
            self.rect.y -= PADDLE_SPEED
        if keys[self.down_key]:
            self.rect.y += PADDLE_SPEED
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_HEIGHT - PADDLE_DIMS[1]:
            self.rect.y = SCREEN_HEIGHT - PADDLE_DIMS[1]


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS, BALL_RADIUS))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = BALL_SPEED.copy()

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT - BALL_RADIUS:
            self.speed[1] *= -1

    def reset_ball(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = [
            random.choice((-1, 1)) * BALL_SPEED[0],
            random.choice((-1, 1)) * BALL_SPEED[1],
        ]


class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.init_assets()

    def init_assets(self):
        self.ball_sprite = Ball()
        self.left_paddle_sprite = Paddle(0, SCREEN_HEIGHT // 2, pygame.K_w, pygame.K_s)
        self.right_paddle_sprite = Paddle(
            SCREEN_WIDTH - PADDLE_DIMS[0],
            SCREEN_HEIGHT // 2,
            pygame.K_UP,
            pygame.K_DOWN,
        )
        self.left_score = 0
        self.right_score = 0

    def reset_game(self):
        self.ball_sprite.reset_ball()
        self.left_score = 0
        self.right_score = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK)

            if pygame.sprite.collide_rect(
                self.ball_sprite, self.left_paddle_sprite
            ) or pygame.sprite.collide_rect(self.ball_sprite, self.right_paddle_sprite):
                self.ball_sprite.speed[0] *= -1

            if self.ball_sprite.rect.x < 0:
                self.right_score += 1
                self.ball_sprite.reset_ball()

            if self.ball_sprite.rect.x > SCREEN_WIDTH:
                self.left_score += 1
                self.ball_sprite.reset_ball()

            score_text = self.font.render(
                f"{self.left_score} - {self.right_score}", True, WHITE
            )
            self.screen.blit(
                score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10)
            )

            self.ball_sprite.update()
            self.left_paddle_sprite.update()
            self.right_paddle_sprite.update()

            self.screen.blit(self.ball_sprite.image, self.ball_sprite.rect)
            self.screen.blit(
                self.left_paddle_sprite.image, self.left_paddle_sprite.rect
            )
            self.screen.blit(
                self.right_paddle_sprite.image, self.right_paddle_sprite.rect
            )

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = PongGame()
    game.run()
