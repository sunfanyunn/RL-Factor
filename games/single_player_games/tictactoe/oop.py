import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
OFFSET = 100
CELL_SIZE = SCREEN_HEIGHT // 3
LINE_WIDTH = 10
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = CELL_SIZE // 4

WHITE = (255, 255, 255)
LINE_COLOR = (23, 85, 85)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (85, 170, 85)
BUTTON_COLOR = (70, 130, 180)


class CrossSprite(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = pygame.Surface(
            (CELL_SIZE - 2 * SPACE, CELL_SIZE - 2 * SPACE), pygame.SRCALPHA
        )
        pygame.draw.line(
            self.image,
            CROSS_COLOR,
            (0, 0),
            (CELL_SIZE - 2 * SPACE, CELL_SIZE - 2 * SPACE),
            CROSS_WIDTH,
        )
        pygame.draw.line(
            self.image,
            CROSS_COLOR,
            (0, CELL_SIZE - 2 * SPACE),
            (CELL_SIZE - 2 * SPACE, 0),
            CROSS_WIDTH,
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)


class CircleSprite(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = pygame.Surface(
            (CELL_SIZE - 2 * SPACE, CELL_SIZE - 2 * SPACE), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image,
            CIRCLE_COLOR,
            (CELL_SIZE // 2 - SPACE, CELL_SIZE // 2 - SPACE),
            CIRCLE_RADIUS,
            CIRCLE_WIDTH,
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)


class TicTacToeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + OFFSET))
        pygame.display.set_caption("Tic Tac Toe")
        self.cross_sprites = pygame.sprite.Group()
        self.circle_sprites = pygame.sprite.Group()

    def render_background(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "X":
                    cross_sprite = CrossSprite(row, col)
                    self.cross_sprites.add(cross_sprite)
                elif self.board[row][col] == "O":
                    circle_sprite = CircleSprite(row, col)
                    self.circle_sprites.add(circle_sprite)

    def init_assets(self):
        self.board = [["" for x in range(3)] for y in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.restart_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT + 20, 140, 50
        )

    def check_win(self):

        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        return None

    def reset_game(self):
        self.init_assets()
        self.cross_sprites.empty()  # Clear the cross sprites
        self.circle_sprites.empty()  # Clear the circle sprites
        self.screen.fill(WHITE)
        self.render_lines()
        pygame.display.update()

    def handle_click(self, pos):
        if self.game_over:
            if self.restart_button.collidepoint(pos):
                self.reset_game()
                return

        col = pos[0] // CELL_SIZE
        row = pos[1] // CELL_SIZE

        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            winner = self.check_win()
            if winner or all(
                self.board[i][j] != "" for i in range(3) for j in range(3)
            ):
                self.game_over = True
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def display_winner(self):
        if self.game_over:
            winner = self.check_win()
            if winner:
                font_winner = pygame.font.SysFont(None, 72)
                text_winner = font_winner.render(f"{winner} Wins!", True, LINE_COLOR)

                text_winner_pos = text_winner.get_rect(
                    center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                )
                self.screen.blit(text_winner, text_winner_pos)
            else:
                font_draw = pygame.font.SysFont(None, 72)
                text_draw = font_draw.render("Draw!", True, LINE_COLOR)
                text_draw_pos = text_draw.get_rect(
                    center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                )
                self.screen.blit(text_draw, text_draw_pos)

            pygame.draw.rect(self.screen, BUTTON_COLOR, self.restart_button)
            font = pygame.font.SysFont(None, 36)
            text = font.render("Restart", True, WHITE)
            self.screen.blit(
                text, (self.restart_button.x + 50, self.restart_button.y + 10)
            )

    def render_lines(self):
        pygame.draw.line(
            self.screen,
            LINE_COLOR,
            (SCREEN_WIDTH // 3, 0),
            (SCREEN_WIDTH // 3, SCREEN_HEIGHT),
            LINE_WIDTH,
        )
        pygame.draw.line(
            self.screen,
            LINE_COLOR,
            (2 * SCREEN_WIDTH // 3, 0),
            (2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT),
            LINE_WIDTH,
        )
        pygame.draw.line(
            self.screen,
            LINE_COLOR,
            (0, SCREEN_HEIGHT // 3),
            (SCREEN_WIDTH, SCREEN_HEIGHT // 3),
            LINE_WIDTH,
        )
        pygame.draw.line(
            self.screen,
            LINE_COLOR,
            (0, 2 * SCREEN_HEIGHT // 3),
            (SCREEN_WIDTH, 2 * SCREEN_HEIGHT // 3),
            LINE_WIDTH,
        )

    def run(self):
        self.init_assets()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.screen.fill(WHITE)
            self.render_lines()
            self.render_background()
            self.cross_sprites.draw(self.screen)
            self.circle_sprites.draw(self.screen)
            self.display_winner()
            pygame.display.update()


if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()
