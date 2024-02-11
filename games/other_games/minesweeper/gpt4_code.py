import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
EMPTY = 0
HAZARD = 1
REVEALED = 2
NUM_HAZARDS = 10


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def init_assets(self):
        self.board = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.revealed = [[False for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.place_hazards()
        self.game_over = False
        self.player_won = False

    def place_hazards(self):
        for _ in range(NUM_HAZARDS):
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            while self.board[y][x] == HAZARD:
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(
                    0, GRID_SIZE - 1
                )
            self.board[y][x] = HAZARD

    def check_win(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.board[y][x] != HAZARD and not self.revealed[y][x]:
                    return False
        return True

    def reveal_cell(self, row, col):
        if self.revealed[row][col]:
            return
        self.revealed[row][col] = True
        if self.board[row][col] == HAZARD:
            self.game_over = True
            return
        count = self.surrounding_count(row, col)
        self.board[row][col] = count
        if count == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if 0 <= row + dy < GRID_SIZE and 0 <= col + dx < GRID_SIZE:
                        self.reveal_cell(row + dy, col + dx)

    def surrounding_count(self, row, col):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if (
                    0 <= row + dy < GRID_SIZE
                    and 0 <= col + dx < GRID_SIZE
                    and self.board[row + dy][col + dx] == HAZARD
                ):
                    count += 1
        return count

    def run(self):
        self.init_assets()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col, row = x // CELL_SIZE, y // CELL_SIZE
                    self.reveal_cell(row, col)
                    if self.check_win():
                        self.game_over = True
                        self.player_won = True
            self.draw()
            pygame.display.flip()

    def draw(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.revealed[y][x]:
                    if self.board[y][x] == HAZARD:
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)
                    else:
                        pygame.draw.rect(self.screen, (200, 200, 200), rect)
                        if self.board[y][x] > 0:
                            font = pygame.font.Font(None, CELL_SIZE // 2)
                            text = font.render(str(self.board[y][x]), 1, (10, 10, 10))
                            self.screen.blit(
                                text,
                                (
                                    x * CELL_SIZE + CELL_SIZE // 3,
                                    y * CELL_SIZE + CELL_SIZE // 3,
                                ),
                            )
                else:
                    pygame.draw.rect(self.screen, (100, 100, 100), rect)


if __name__ == "__main__":
    game = Game()
    game.run()
