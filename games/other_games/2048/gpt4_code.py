import pygame
import sys
import time
import random
from pygame.locals import *

WHITE = (255, 255, 255)
GREEN = (77, 204, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Game_2048:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((450, 600))
        pygame.display.set_caption("2048")

        self.myfont = pygame.font.SysFont(None, 50)
        self.score = 0
        self.board = self.init_board()
        self.reset_button = pygame.Rect(
            175, 550, 100, 40
        )  # Define the reset button rectangle

    def init_board(self):
        """
        Init game
        """
        self.board = [[0] * 4 for _ in range(4)]
        self.add_new_num(2)

    def add_new_num(self, n):
        """
        Add new number to the board
        """
        empty_cells = [
            (i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0
        ]
        (i, j) = random.choice(empty_cells)
        self.board[i][j] = n

    def check_win(self):
        """
        Check if the player has won
        """
        return any(max(row) == 2048 for row in self.board)

    def can_move(self):
        """
        Check if the player can move
        """
        return any(self.board[i][j] == 0 for i in range(4) for j in range(4))

    def check_lose(self):
        """
        Check if the player has lost
        """
        return not self.can_move() and not any(
            self.board[i][j] == self.board[i + 1][j]
            or self.board[i][j] == self.board[i][j + 1]
            for i in range(3)
            for j in range(3)
        )

    def main(self, UserInput):
        """
        This function should update the game board based on the user input.
        """
        # Implement the logic to update the game board based on the user input

    def update_score(self, move):

        """
        Update the score when tiles are merged
        """

    # Implement the logic to update the score when tiles are merged

    def reset(self):
        """
        Reset the game board and score
        """
        self.score = 0
        self.board = self.init_board()

    def run(self):
        """
        please implement the main game loop here
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.reset_button.collidepoint(mouse_pos):
                        self.reset()
                elif event.type == KEYDOWN:
                    if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                        self.main(event.key)
                        if self.check_win():
                            print("You win!")
                            self.reset()
                        elif self.check_lose():
                            print("You lose!")
                            self.reset()
            pygame.display.update()
            time.sleep(0.1)


if __name__ == "__main__":
    game = Game_2048()
    game.run()
