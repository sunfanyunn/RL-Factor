import pygame
import sys
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PAUSE_GAME = 1000
BALL_RADIUS = 15
BALL_SPEED = [3, 3]
PADDLE_SPEED = 5
PADDLE_DIMS = [10, 60]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_DIMS = [140, 40]
BUTTON_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (100, 100, 100)


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
        if keys[self.up_key] and self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED
        if keys[self.down_key] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PADDLE_SPEED


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        self.rect.move_ip(*BALL_SPEED)

        if self.rect.right >= SCREEN_WIDTH:
            self.game.left_score += 1
            self.reset_ball()
        elif self.rect.left <= 0:
            self.game.right_score += 1
            self.reset_ball()
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            BALL_SPEED[1] = -BALL_SPEED[1]
        if self.rect.colliderect(
            self.game.left_paddle_sprite.rect
        ) or self.rect.colliderect(self.game.right_paddle_sprite.rect):
            BALL_SPEED[0] = -BALL_SPEED[0]

    def reset_ball(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        BALL_SPEED[0] = -BALL_SPEED[0]
        pygame.time.wait(PAUSE_GAME)


class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.font = pygame.font.Font(None, 36)
        self.all_sprites = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()
        self.ball = pygame.sprite.GroupSingle()
        self.init_assets()

    def init_assets(self):
        self.left_paddle_sprite = Paddle(
            0, SCREEN_HEIGHT // 2 - PADDLE_DIMS[1] // 2, pygame.K_w, pygame.K_s
        )
        self.right_paddle_sprite = Paddle(
            SCREEN_WIDTH - PADDLE_DIMS[0],
            SCREEN_HEIGHT // 2 - PADDLE_DIMS[1] // 2,
            pygame.K_UP,
            pygame.K_DOWN,
        )

        self.ball_sprite = Ball()
        self.ball_sprite.game = self

        self.paddles.add(self.left_paddle_sprite, self.right_paddle_sprite)
        self.ball.add(self.ball_sprite)
        self.all_sprites.add(
            self.left_paddle_sprite, self.right_paddle_sprite, self.ball_sprite
        )
        self.reset_button = pygame.Rect(
            (SCREEN_WIDTH - BUTTON_DIMS[0]) // 2, SCREEN_HEIGHT - 50, *BUTTON_DIMS
        )

        self.left_score = 0
        self.right_score = 0

    def reset_game(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.reset_button.collidepoint(
            event.pos
        ):
            self.all_sprites.empty()
            self.init_assets()

    def render_game(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        color = (
            HIGHLIGHT_COLOR
            if self.reset_button.collidepoint(mouse_pos)
            else BUTTON_COLOR
        )
        pygame.draw.rect(self.screen, color, self.reset_button)
        button_text = self.font.render("Reset Scores", True, WHITE)
        self.screen.blit(
            button_text,
            (
                self.reset_button.x + (BUTTON_DIMS[0] - button_text.get_width()) // 2,
                self.reset_button.y + (BUTTON_DIMS[1] - button_text.get_height()) // 2,
            ),
        )

        score_display = self.font.render(
            f"{self.left_score} - {self.right_score}", True, WHITE
        )
        self.screen.blit(
            score_display, (SCREEN_WIDTH // 2 - score_display.get_width() // 2, 10)
        )
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.reset_game(event)
            self.paddles.update()
            self.ball.update()
            self.render_game()
            pygame.time.Clock().tick(60)


if __name__ == "__main__":
    game = PongGame()
    game.run()
