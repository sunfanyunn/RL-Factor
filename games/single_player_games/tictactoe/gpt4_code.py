import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
OFFSET = 100


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + OFFSET))
        self.font = pygame.font.Font(None, 48)
        self.clock = pygame.time.Clock()

    def init_assets(self):
        self.board = [["" for x in range(3)] for y in range(3)]
        self.current_player = "X"
        self.game_over = False

    def handle_click(self, pos):
        if self.game_over:
            return
        x, y = pos[0] // 200, pos[1] // 200
        if self.board[y][x] == "":
            self.board[y][x] = self.current_player
            if self.check_win():
                self.game_over = True
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_win(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def reset_game(self):
        self.init_assets()

    def run(self):
        self.init_assets()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
            self.screen.fill((255, 255, 255))
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == "X":
                        pygame.draw.line(
                            self.screen,
                            (255, 0, 0),
                            (x * 200 + 50, y * 200 + 50),
                            (x * 200 + 150, y * 200 + 150),
                            25,
                        )
                        pygame.draw.line(
                            self.screen,
                            (255, 0, 0),
                            (x * 200 + 150, y * 200 + 50),
                            (x * 200 + 50, y * 200 + 150),
                            25,
                        )
                    elif self.board[y][x] == "O":
                        pygame.draw.circle(
                            self.screen,
                            (0, 0, 255),
                            (x * 200 + 100, y * 200 + 100),
                            50,
                            25,
                        )
            if self.game_over:
                text = self.font.render(
                    "Player {} wins! Press R to restart".format(self.current_player),
                    True,
                    (0, 0, 0),
                )
                self.screen.blit(
                    text,
                    (
                        SCREEN_WIDTH // 2 - text.get_width() // 2,
                        SCREEN_HEIGHT + OFFSET // 2 - text.get_height() // 2,
                    ),
                )
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
