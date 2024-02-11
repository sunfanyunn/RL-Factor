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
        self.window = pygame.display.set_mode(
            (450, 600)
        )  # Increase window height for the reset button
        pygame.display.set_caption("2048")

        self.myfont = pygame.font.SysFont(None, 50)
        self.score = 0  # Track the score
        self.board = self.init_board()
        self.reset_button = pygame.Rect(
            175, 550, 100, 40
        )  # Define the reset button rectangle

    def init_board(self):
        self.board = []
        for i in range(4):
            self.board += [["0"] * 4]
        self.add_new_num(2)
        return self.board

    def add_new_num(self, n):
        for i in range(n):
            newNum = str(random.choice([2, 4]))
            randomx = random.randrange(4)
            randomy = random.randrange(4)
            while self.board[randomy][randomx] != "0":
                randomx = random.randrange(4)
                randomy = random.randrange(4)
            self.board[randomy][randomx] = newNum

    def check_win(self):
        win = False
        for line in self.board:
            for num in line:
                if num == "2048":
                    win = True
        return win

    def add(self, i_list, j_list, i_direction, j_direction):
        move = 0
        for i in i_list:
            for j in j_list:
                if self.board[i][j] == self.board[i + i_direction][j + j_direction]:
                    self.board[i + i_direction][j + j_direction] = str(
                        int(self.board[i][j])
                        + int(self.board[i + i_direction][j + j_direction])
                    )
                    if self.board[i][j] != "0":
                        move += 1
                    self.board[i][j] = "0"
        return move

    def push(self, i_list, j_list, i_direction, j_direction):
        move = 0
        for i in i_list:
            for j in j_list:
                if self.board[i + i_direction][j + j_direction] == "0":
                    self.board[i + i_direction][j + j_direction] = self.board[i][j]
                    if self.board[i][j] != "0":
                        move += 1
                    self.board[i][j] = "0"
        return move

    def push_direction(self, UserInput):
        move = 0
        if UserInput == "u":
            i_list, j_list = range(1, 4), range(4)
            i_direction, j_direction = -1, 0
        elif UserInput == "d":
            i_list, j_list = range(2, -1, -1), range(4)
            i_direction, j_direction = 1, 0
        elif UserInput == "l":
            i_list, j_list = range(4), range(1, 4)
            i_direction, j_direction = 0, -1
        elif UserInput == "r":
            i_list, j_list = range(4), range(2, -1, -1)
            i_direction, j_direction = 0, 1

        for i in range(4):
            move += self.push(i_list, j_list, i_direction, j_direction)
        move += self.add(i_list, j_list, i_direction, j_direction)
        for i in range(4):
            move += self.push(i_list, j_list, i_direction, j_direction)

        return move

    def check_cell(self, i, j):
        move_i = []
        move_j = []
        board_size = len(self.board)
        if i > 0:
            move_i.append(-1)
            move_j.append(0)
        if i < (board_size - 1):
            move_i.append(1)
            move_j.append(0)
        if j > 0:
            move_j.append(-1)
            move_i.append(0)
        if j < (board_size - 1):
            move_j.append(1)
            move_i.append(0)
        for k in range(len(move_i)):
            if self.board[i + move_i[k]][j + move_j[k]] == self.board[i][j]:
                return True
        return False

    def can_move(self):
        board_size = len(self.board)
        for i in range(board_size):
            for j in range(board_size):
                if self.board[i][j] == "0":
                    return True
                if self.check_cell(i, j):
                    return True
        return False

    def check_lose(self):
        nozero = False
        for elt in self.board:
            nozero = nozero or ("0" in elt)

        if not nozero:
            return not self.can_move()
        return False

    def main(self, UserInput):

        if not self.check_lose() and not self.check_win():
            move = self.push_direction(UserInput)
            if move != 0:
                self.add_new_num(1)
                self.update_score(move)  # Update the score
        return self.board

    def update_score(self, move):
        # Update the score when tiles are merged
        self.score += move

    def reset(self):
        # Reset the game board and score
        self.board = self.init_board()
        self.score = 0

    def build_text(self, i, j):
        if self.board[j][i] == "0":
            text = self.myfont.render(" ", True, BLUE)
        else:
            text = self.myfont.render(self.board[j][i], True, BLUE)
        textRect = text.get_rect()
        textRect.centerx = i * 100 + 75
        textRect.centery = j * 100 + 180
        return text, textRect

    def show_text(self):
        for i in range(4):
            for j in range(4):
                self.window.blit(self.build_text(i, j)[0], self.build_text(i, j)[1])

    def quit_window(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    def game_over(self):
        label = self.myfont.render("GAME OVER", True, RED)
        labelRect = label.get_rect()
        labelRect.centerx = self.window.get_rect().centerx
        labelRect.centery = self.window.get_rect().centery
        self.window.blit(label, labelRect)
        event = pygame.event.wait()
        self.quit_window(event)

    def win(self):
        self.window.fill(WHITE)
        label = self.myfont.render("You WIN !!!!!", True, RED)
        labelRect = label.get_rect()
        labelRect.centerx = self.window.get_rect().centerx
        labelRect.centery = self.window.get_rect().centery
        self.window.blit(label, labelRect)
        event = pygame.event.wait()
        self.quit_window(event)

    def run(self):
        blocks = []
        for i in range(4):
            for j in range(4):
                blocks.append(
                    [pygame.Rect((i * 100) + 30, (j * 100) + 135, 90, 90), WHITE]
                )

        while True:
            for event in pygame.event.get():
                self.quit_window(event)
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.board = self.main("u")
                    if event.key == K_DOWN:
                        self.board = self.main("d")
                    if event.key == K_LEFT:
                        self.board = self.main("l")
                    if event.key == K_RIGHT:
                        self.board = self.main("r")

                if (
                    event.type == MOUSEBUTTONDOWN and event.button == 1
                ):  # Check for left mouse button click
                    if self.reset_button.collidepoint(event.pos):
                        self.reset()  # Reset the game when the reset button is clicked

            self.window.fill(WHITE)
            header = self.myfont.render("2048", True, BLUE)
            self.window.blit(header, (30, 50))
            pygame.draw.rect(self.window, GREEN, pygame.Rect(20, 125, 410, 410))

            for block in blocks:
                pygame.draw.rect(self.window, block[1], block[0])
            self.show_text()

            # Draw the reset button
            pygame.draw.rect(self.window, RED, self.reset_button)
            reset_label = self.myfont.render("Reset", True, WHITE)
            reset_label_rect = reset_label.get_rect()
            reset_label_rect.center = self.reset_button.center
            self.window.blit(reset_label, reset_label_rect)

            # Draw the score on the screen
            score_label = self.myfont.render(f"Score: {self.score}", True, BLUE)
            self.window.blit(score_label, (250, 50))

            if self.check_lose():
                self.game_over()
            elif self.check_win():
                self.win()

            pygame.display.update()
            time.sleep(0.02)


if __name__ == "__main__":
    game = Game_2048()
    game.run()
