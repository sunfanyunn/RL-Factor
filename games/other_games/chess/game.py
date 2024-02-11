import pygame
from pygame.locals import *
import random
import os
import time
import queue


class Chess(object):
    def __init__(self, screen, pieces_src, square_coords, square_length):
        self.screen = screen
        self.chess_pieces = Piece(pieces_src, cols=6, rows=2)
        self.board_locations = square_coords
        self.square_length = square_length
        self.turn = {"black": 0, "white": 0}
        self.moves = []
        self.utils = Utils()
        self.pieces = {
            "white_pawn": 5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook": 4,
            "white_king": 0,
            "white_queen": 1,
            "black_pawn": 11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook": 10,
            "black_king": 6,
            "black_queen": 7,
        }
        self.captured = []
        self.winner = ""
        self.reset()

    def reset(self):
        self.moves = []
        x = random.randint(0, 1)
        if x == 1:
            self.turn["black"] = 1
        elif x == 0:
            self.turn["white"] = 1
        self.piece_location = {}
        x = 0
        for i in range(97, 105):
            a = 8
            y = 0
            self.piece_location[chr(i)] = {}
            while a > 0:
                self.piece_location[chr(i)][a] = ["", False, [x, y]]
                a = a - 1
                y = y + 1
            x = x + 1
        for i in range(97, 105):
            x = 8
            while x > 0:
                if x == 8:
                    if chr(i) == "a" or chr(i) == "h":
                        self.piece_location[chr(i)][x][0] = "black_rook"
                    elif chr(i) == "b" or chr(i) == "g":
                        self.piece_location[chr(i)][x][0] = "black_knight"
                    elif chr(i) == "c" or chr(i) == "f":
                        self.piece_location[chr(i)][x][0] = "black_bishop"
                    elif chr(i) == "d":
                        self.piece_location[chr(i)][x][0] = "black_queen"
                    elif chr(i) == "e":
                        self.piece_location[chr(i)][x][0] = "black_king"
                elif x == 7:
                    self.piece_location[chr(i)][x][0] = "black_pawn"
                elif x == 2:
                    self.piece_location[chr(i)][x][0] = "white_pawn"
                elif x == 1:
                    if chr(i) == "a" or chr(i) == "h":
                        self.piece_location[chr(i)][x][0] = "white_rook"
                    elif chr(i) == "b" or chr(i) == "g":
                        self.piece_location[chr(i)][x][0] = "white_knight"
                    elif chr(i) == "c" or chr(i) == "f":
                        self.piece_location[chr(i)][x][0] = "white_bishop"
                    elif chr(i) == "d":
                        self.piece_location[chr(i)][x][0] = "white_queen"
                    elif chr(i) == "e":
                        self.piece_location[chr(i)][x][0] = "white_king"
                x = x - 1

    def play_turn(self):
        white_color = (255, 255, 255)
        small_font = pygame.font.SysFont("comicsansms", 20)
        if self.turn["black"]:
            turn_text = small_font.render("Turn: Black", True, white_color)
        elif self.turn["white"]:
            turn_text = small_font.render("Turn: White", True, white_color)
        self.screen.blit(
            turn_text, ((self.screen.get_width() - turn_text.get_width()) // 2, 10)
        )
        if self.turn["black"]:
            self.move_piece("black")
        elif self.turn["white"]:
            self.move_piece("white")

    def draw_pieces(self):
        transparent_green = (0, 194, 39, 170)
        transparent_blue = (28, 21, 212, 170)
        surface = pygame.Surface(
            (self.square_length, self.square_length), pygame.SRCALPHA
        )
        surface.fill(transparent_green)
        surface1 = pygame.Surface(
            (self.square_length, self.square_length), pygame.SRCALPHA
        )
        surface1.fill(transparent_blue)
        for val in self.piece_location.values():
            for value in val.values():
                piece_name = value[0]
                piece_coord_x, piece_coord_y = value[2]
                if value[1] and len(value[0]) > 5:
                    if value[0][:5] == "black":
                        self.screen.blit(
                            surface, self.board_locations[piece_coord_x][piece_coord_y]
                        )
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if (
                                    x_coord >= 0
                                    and y_coord >= 0
                                    and x_coord < 8
                                    and y_coord < 8
                                ):
                                    self.screen.blit(
                                        surface, self.board_locations[x_coord][y_coord]
                                    )
                    elif value[0][:5] == "white":
                        self.screen.blit(
                            surface1, self.board_locations[piece_coord_x][piece_coord_y]
                        )
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if (
                                    x_coord >= 0
                                    and y_coord >= 0
                                    and x_coord < 8
                                    and y_coord < 8
                                ):
                                    self.screen.blit(
                                        surface1, self.board_locations[x_coord][y_coord]
                                    )
        for val in self.piece_location.values():
            for value in val.values():
                piece_name = value[0]
                piece_coord_x, piece_coord_y = value[2]
                if len(value[0]) > 1:
                    self.chess_pieces.draw(
                        self.screen,
                        piece_name,
                        self.board_locations[piece_coord_x][piece_coord_y],
                    )

    def possible_moves(self, piece_name, piece_coord):
        positions = []
        if len(piece_name) > 0:
            x_coord, y_coord = piece_coord
            if piece_name[6:] == "bishop":
                positions = self.diagonal_moves(positions, piece_name, piece_coord)
            elif piece_name[6:] == "pawn":
                columnChar = chr(97 + x_coord)
                rowNo = 8 - y_coord
                if piece_name == "black_pawn":
                    if y_coord + 1 < 8:
                        rowNo = rowNo - 1
                        front_piece = self.piece_location[columnChar][rowNo][0]
                        if front_piece[6:] != "pawn":
                            positions.append([x_coord, y_coord + 1])
                            if y_coord < 2:
                                positions.append([x_coord, y_coord + 2])
                        if x_coord - 1 >= 0 and y_coord + 1 < 8:
                            x = x_coord - 1
                            y = y_coord + 1
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]
                            if to_capture[0][:5] == "white":
                                positions.append([x, y])
                        if x_coord + 1 < 8 and y_coord + 1 < 8:
                            x = x_coord + 1
                            y = y_coord + 1
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]
                            if to_capture[0][:5] == "white":
                                positions.append([x, y])
                elif piece_name == "white_pawn":
                    if y_coord - 1 >= 0:
                        rowNo = rowNo + 1
                        front_piece = self.piece_location[columnChar][rowNo][0]
                        if front_piece[6:] != "pawn":
                            positions.append([x_coord, y_coord - 1])
                            if y_coord > 5:
                                positions.append([x_coord, y_coord - 2])
                        if x_coord - 1 >= 0 and y_coord - 1 >= 0:
                            x = x_coord - 1
                            y = y_coord - 1
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]
                            if to_capture[0][:5] == "black":
                                positions.append([x, y])
                        if x_coord + 1 < 8 and y_coord - 1 >= 0:
                            x = x_coord + 1
                            y = y_coord - 1
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]
                            if to_capture[0][:5] == "black":
                                positions.append([x, y])
            elif piece_name[6:] == "rook":
                positions = self.linear_moves(positions, piece_name, piece_coord)
            elif piece_name[6:] == "knight":
                if (x_coord - 2) >= 0:
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord - 2, y_coord - 1])
                    if (y_coord + 1) < 8:
                        positions.append([x_coord - 2, y_coord + 1])
                if (y_coord - 2) >= 0:
                    if (x_coord - 1) >= 0:
                        positions.append([x_coord - 1, y_coord - 2])
                    if (x_coord + 1) < 8:
                        positions.append([x_coord + 1, y_coord - 2])
                if (x_coord + 2) < 8:
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord + 2, y_coord - 1])
                    if (y_coord + 1) < 8:
                        positions.append([x_coord + 2, y_coord + 1])
                if (y_coord + 2) < 8:
                    if (x_coord - 1) >= 0:
                        positions.append([x_coord - 1, y_coord + 2])
                    if (x_coord + 1) < 8:
                        positions.append([x_coord + 1, y_coord + 2])
            elif piece_name[6:] == "king":
                if (y_coord - 1) >= 0:
                    positions.append([x_coord, y_coord - 1])
                if (y_coord + 1) < 8:
                    positions.append([x_coord, y_coord + 1])
                if (x_coord - 1) >= 0:
                    positions.append([x_coord - 1, y_coord])
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord - 1, y_coord - 1])
                    if (y_coord + 1) < 8:
                        positions.append([x_coord - 1, y_coord + 1])
                if (x_coord + 1) < 8:
                    positions.append([x_coord + 1, y_coord])
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord + 1, y_coord - 1])
                    if (y_coord + 1) < 8:
                        positions.append([x_coord + 1, y_coord + 1])
            elif piece_name[6:] == "queen":
                positions = self.diagonal_moves(positions, piece_name, piece_coord)
                positions = self.linear_moves(positions, piece_name, piece_coord)
            to_remove = []
            for pos in positions:
                x, y = pos
                columnChar = chr(97 + x)
                rowNo = 8 - y
                des_piece_name = self.piece_location[columnChar][rowNo][0]
                if des_piece_name[:5] == piece_name[:5]:
                    to_remove.append(pos)
            for i in to_remove:
                positions.remove(i)
        return positions

    def move_piece(self, turn):
        square = self.get_selected_square()
        if square:
            piece_name = square[0]
            piece_color = piece_name[:5]
            columnChar = square[1]
            rowNo = square[2]
            x, y = self.piece_location[columnChar][rowNo][2]
            if (len(piece_name) > 0) and (piece_color == turn):
                self.moves = self.possible_moves(piece_name, [x, y])
            p = self.piece_location[columnChar][rowNo]
            for i in self.moves:
                if i == [x, y]:
                    if (p[0][:5] == turn) or len(p[0]) == 0:
                        self.validate_move([x, y])
                    else:
                        self.capture_piece(turn, [columnChar, rowNo], [x, y])
            if piece_color == turn:
                for k in self.piece_location.keys():
                    for key in self.piece_location[k].keys():
                        self.piece_location[k][key][1] = False
                self.piece_location[columnChar][rowNo][1] = True

    def get_selected_square(self):
        left_click = self.utils.left_click_event()
        if left_click:
            mouse_event = self.utils.get_mouse_event()
            for i in range(len(self.board_locations)):
                for j in range(len(self.board_locations)):
                    rect = pygame.Rect(
                        self.board_locations[i][j][0],
                        self.board_locations[i][j][1],
                        self.square_length,
                        self.square_length,
                    )
                    collision = rect.collidepoint(mouse_event[0], mouse_event[1])
                    if collision:
                        selected = [rect.x, rect.y]
                        for k in range(len(self.board_locations)):
                            try:
                                l = None
                                l = self.board_locations[k].index(selected)
                                if l != None:
                                    for val in self.piece_location.values():
                                        for value in val.values():
                                            if not value[1]:
                                                value[1] = False
                                    columnChar = chr(97 + k)
                                    rowNo = 8 - l
                                    piece_name = self.piece_location[columnChar][rowNo][
                                        0
                                    ]
                                    return [piece_name, columnChar, rowNo]
                            except:
                                pass
        else:
            return None

    def capture_piece(self, turn, chess_board_coord, piece_coord):
        x, y = piece_coord
        columnChar, rowNo = chess_board_coord
        p = self.piece_location[columnChar][rowNo]
        if p[0] == "white_king":
            self.winner = "Black"
            print("Black wins")
        elif p[0] == "black_king":
            self.winner = "White"
            print("White wins")
        self.captured.append(p)
        self.validate_move(piece_coord)

    def validate_move(self, destination):
        desColChar = chr(97 + destination[0])
        desRowNo = 8 - destination[1]
        for k in self.piece_location.keys():
            for key in self.piece_location[k].keys():
                board_piece = self.piece_location[k][key]
                if board_piece[1]:
                    self.piece_location[k][key][1] = False
                    piece_name = self.piece_location[k][key][0]
                    self.piece_location[desColChar][desRowNo][0] = piece_name
                    src_name = self.piece_location[k][key][0]
                    self.piece_location[k][key][0] = ""
                    if self.turn["black"]:
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                    elif "white":
                        self.turn["black"] = 1
                        self.turn["white"] = 0
                    src_location = k + str(key)
                    des_location = desColChar + str(desRowNo)
                    print(
                        "{} moved from {} to {}".format(
                            src_name, src_location, des_location
                        )
                    )

    def diagonal_moves(self, positions, piece_name, piece_coord):
        x, y = piece_coord
        while True:
            x = x - 1
            y = y - 1
            if x < 0 or y < 0:
                break
            else:
                positions.append([x, y])
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
        x, y = piece_coord
        while True:
            x = x + 1
            y = y + 1
            if x > 7 or y > 7:
                break
            else:
                positions.append([x, y])
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
        x, y = piece_coord
        while True:
            x = x - 1
            y = y + 1
            if x < 0 or y > 7:
                break
            else:
                positions.append([x, y])
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
        x, y = piece_coord
        while True:
            x = x + 1
            y = y - 1
            if x > 7 or y < 0:
                break
            else:
                positions.append([x, y])
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
        return positions

    def linear_moves(self, positions, piece_name, piece_coord):
        x, y = piece_coord
        while x > 0:
            x = x - 1
            positions.append([x, y])
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
        x, y = piece_coord
        while x < 7:
            x = x + 1
            positions.append([x, y])
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
        x, y = piece_coord
        while y > 0:
            y = y - 1
            positions.append([x, y])
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
        x, y = piece_coord
        while y < 7:
            y = y + 1
            positions.append([x, y])
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
        return positions


class Game:
    def __init__(self):
        screen_width = 640
        screen_height = 750
        self.menu_showed = False
        self.running = True
        self.resources = "res"
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        window_title = "Chess"
        pygame.display.set_caption(window_title)
        icon_src = os.path.join(self.resources, "chess_icon.png")
        icon = pygame.image.load(icon_src)
        pygame.display.set_icon(icon)
        pygame.display.flip()
        self.clock = pygame.time.Clock()

    def start_game(self):
        """Function containing main game loop"""
        self.board_offset_x = 0
        self.board_offset_y = 50
        self.board_dimensions = (self.board_offset_x, self.board_offset_y)
        board_src = os.path.join(self.resources, "board.png")
        self.board_img = pygame.image.load(board_src).convert()
        square_length = self.board_img.get_rect().width // 8
        self.board_locations = []
        for x in range(0, 8):
            self.board_locations.append([])
            for y in range(0, 8):
                self.board_locations[x].append(
                    [
                        self.board_offset_x + (x * square_length),
                        self.board_offset_y + (y * square_length),
                    ]
                )
        pieces_src = os.path.join(self.resources, "pieces.png")
        self.chess = Chess(self.screen, pieces_src, self.board_locations, square_length)
        while self.running:
            self.clock.tick(5)
            for event in pygame.event.get():
                key_pressed = pygame.key.get_pressed()
                if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                    self.running = False
                elif key_pressed[K_SPACE]:
                    self.chess.reset()
            winner = self.chess.winner
            if self.menu_showed == False:
                self.menu()
            elif len(winner) > 0:
                self.declare_winner(winner)
            else:
                self.game()
            pygame.display.flip()
            pygame.event.pump()
        pygame.quit()

    def menu(self):
        """method to show game menu"""
        bg_color = (255, 255, 255)
        self.screen.fill(bg_color)
        black_color = (0, 0, 0)
        start_btn = pygame.Rect(270, 300, 100, 50)
        pygame.draw.rect(self.screen, black_color, start_btn)
        white_color = (255, 255, 255)
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        welcome_text = big_font.render("Chess", False, black_color)
        created_by = small_font.render("Created by Sheriff", True, black_color)
        start_btn_label = small_font.render("Play", True, white_color)
        self.screen.blit(
            welcome_text,
            ((self.screen.get_width() - welcome_text.get_width()) // 2, 150),
        )
        self.screen.blit(
            created_by,
            (
                (self.screen.get_width() - created_by.get_width()) // 2,
                self.screen.get_height() - created_by.get_height() - 100,
            ),
        )
        self.screen.blit(
            start_btn_label,
            (
                (
                    start_btn.x + (start_btn.width - start_btn_label.get_width()) // 2,
                    start_btn.y
                    + (start_btn.height - start_btn_label.get_height()) // 2,
                )
            ),
        )
        key_pressed = pygame.key.get_pressed()
        util = Utils()
        if util.left_click_event():
            mouse_coords = util.get_mouse_event()
            if start_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, start_btn, 3)
                self.menu_showed = True
            elif key_pressed[K_RETURN]:
                self.menu_showed = True

    def game(self):
        color = (0, 0, 0)
        self.screen.fill(color)
        self.screen.blit(self.board_img, self.board_dimensions)
        self.chess.play_turn()
        self.chess.draw_pieces()

    def declare_winner(self, winner):
        bg_color = (255, 255, 255)
        self.screen.fill(bg_color)
        black_color = (0, 0, 0)
        reset_btn = pygame.Rect(250, 300, 140, 50)
        pygame.draw.rect(self.screen, black_color, reset_btn)
        white_color = (255, 255, 255)
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        text = winner + " wins!"
        winner_text = big_font.render(text, False, black_color)
        reset_label = "Play Again"
        reset_btn_label = small_font.render(reset_label, True, white_color)
        self.screen.blit(
            winner_text, ((self.screen.get_width() - winner_text.get_width()) // 2, 150)
        )
        self.screen.blit(
            reset_btn_label,
            (
                (
                    reset_btn.x + (reset_btn.width - reset_btn_label.get_width()) // 2,
                    reset_btn.y
                    + (reset_btn.height - reset_btn_label.get_height()) // 2,
                )
            ),
        )
        key_pressed = pygame.key.get_pressed()
        util = Utils()
        if util.left_click_event():
            mouse_coords = util.get_mouse_event()
            if reset_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                pygame.draw.rect(self.screen, white_color, reset_btn, 3)
                self.menu_showed = False
            elif key_pressed[K_RETURN]:
                self.menu_showed = False
            self.chess.reset()
            self.chess.winner = ""


class Piece(pygame.sprite.Sprite):
    def __init__(self, filename, cols, rows):
        pygame.sprite.Sprite.__init__(self)
        self.pieces = {
            "white_pawn": 5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook": 4,
            "white_king": 0,
            "white_queen": 1,
            "black_pawn": 11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook": 10,
            "black_king": 6,
            "black_queen": 7,
        }
        self.spritesheet = pygame.image.load(filename).convert_alpha()
        self.cols = cols
        self.rows = rows
        self.cell_count = cols * rows
        self.rect = self.spritesheet.get_rect()
        w = self.cell_width = self.rect.width // self.cols
        h = self.cell_height = self.rect.height // self.rows
        self.cells = list(
            [(i % cols * w, i // cols * h, w, h) for i in range(self.cell_count)]
        )

    def draw(self, surface, piece_name, coords):
        piece_index = self.pieces[piece_name]
        surface.blit(self.spritesheet, coords, self.cells[piece_index])


class Utils:
    def get_mouse_event(self):
        # get coordinates of the mouse
        position = pygame.mouse.get_pos()

        # return left click status and mouse coordinates
        return position

    def left_click_event(self):
        # store mouse buttons
        mouse_btn = pygame.mouse.get_pressed()
        # create flag to check for left click event
        left_click = False

        if mouse_btn[0]:  # and e.button == 1:
            # change left click flag
            left_click = True

        return left_click


if __name__ == "__main__":
    game = Game()
    game.start_game()
