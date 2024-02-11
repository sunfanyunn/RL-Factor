import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
RESTART_OFFSET = 50

CELL_SIZE = 30
ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = SCREEN_WIDTH // CELL_SIZE
NUM_BOMBS = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (70, 130, 180)

EMPTY = 0
BOMB = 1
REVEALED = 2
FLAGGED = 3


class Minesweeper:
    def __init__(self, rows=ROWS, cols=COLS, nbombs=NUM_BOMBS):
        self.rows = rows
        self.cols = cols
        self.nbombs = nbombs
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.cols * CELL_SIZE, self.rows * CELL_SIZE + RESTART_OFFSET)
        )
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.init_assets()

    def init_assets(self):
        self.board = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.place_bombs()
        self.game_over = False
        self.player_won = False
        self.restart_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT + 10, 140, 30
        )

    def place_bombs(self):
        for _ in range(self.nbombs):
            x, y = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)
            while self.board[y][x] == BOMB:
                x, y = random.randint(0, self.cols - 1), random.randint(
                    0, self.rows - 1
                )
            self.board[y][x] = BOMB

    def reveal_cell(self, row, col):
        if self.revealed[row][col]:
            return

        self.revealed[row][col] = True

        if self.board[row][col] == BOMB:
            self.game_over = True
            return

        count = self.surrounding_count(row, col)

        if count == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nr, nc = row + dy, col + dx
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal_cell(nr, nc)

    def surrounding_count(self, row, col):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (
                    0 <= row + dy < self.rows
                    and 0 <= col + dx < self.cols
                    and self.board[row + dy][col + dx] == BOMB
                ):
                    count += 1
        return count

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.revealed[r][c] == (self.board[r][c] == BOMB):
                    return False
        return True

    def render_background(self):
        self.screen.fill(BLACK)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.revealed[r][c]:
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                    )

    def render_assets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.revealed[r][c]:
                    if self.board[r][c] == BOMB:
                        pygame.draw.circle(
                            self.screen,
                            RED,
                            (
                                c * CELL_SIZE + CELL_SIZE // 2,
                                r * CELL_SIZE + CELL_SIZE // 2,
                            ),
                            CELL_SIZE // 2 - 5,
                        )
                    else:
                        count = self.surrounding_count(r, c)
                        if count:
                            font = pygame.font.SysFont(None, 36)
                            text = font.render(str(count), True, BLACK)
                            self.screen.blit(
                                text,
                                (
                                    c * CELL_SIZE
                                    + CELL_SIZE // 2
                                    - text.get_width() // 2,
                                    r * CELL_SIZE
                                    + CELL_SIZE // 2
                                    - text.get_height() // 2,
                                ),
                            )
        if self.game_over:
            pygame.draw.rect(self.screen, BUTTON_COLOR, self.restart_button)
            font = pygame.font.SysFont(None, 36)
            if self.player_won:
                text = font.render("You Win!", True, GREEN)
            else:
                text = font.render("Game Over", True, RED)
            self.screen.blit(
                text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT + 5)
            )
        self.draw_grid()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over and self.restart_button.collidepoint(event.pos):
                        self.__init__()
                        continue
                    else:
                        col, row = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                        self.reveal_cell(row, col)
                        if self.check_win():
                            self.player_won = True
                            self.game_over = True
            self.render_background()
            self.render_assets()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Minesweeper()
    game.run()
