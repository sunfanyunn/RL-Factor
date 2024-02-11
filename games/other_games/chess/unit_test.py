import unittest
import pygame
from game import Chess, Piece, Utils, Game


class TestChess(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Chess Test")

    def test_possible_moves(self):
        chess = Chess(self.screen, "", [], 50)
        # Test possible moves for a white pawn
        moves = chess.possible_moves("white_pawn", [3, 3])
        expected_moves = [[3, 4], [3, 5]]
        self.assertListEqual(moves, expected_moves)

    def test_validate_move(self):
        chess = Chess(self.screen, "", [], 50)
        # Test validating a move of a white pawn
        chess.piece_location["d"][2][0] = "white_pawn"
        chess.validate_move([3, 2])
        self.assertEqual(chess.piece_location["d"][2][0], "")
        self.assertEqual(chess.piece_location["d"][3][0], "white_pawn")

    def test_get_selected_square(self):
        chess = Chess(self.screen, "", [], 50)
        # Test selecting a square with a piece
        chess.piece_location["e"][4][0] = "black_king"
        pygame.mouse.set_pos(225, 225)  # Set the mouse position
        selected_square = chess.get_selected_square()
        self.assertEqual(selected_square, ["black_king", "e", 4])

    def test_capture_piece(self):
        chess = Chess(self.screen, "", [], 50)
        # Test capturing a piece
        chess.piece_location["e"][4][0] = "white_queen"
        chess.capture_piece("black", ["e", 4], [5, 5])
        self.assertEqual(chess.piece_location["e"][4][0], "")
        self.assertEqual(chess.piece_location["e"][5][0], "white_queen")

    def test_reset(self):
        chess = Chess(self.screen, "", [], 50)
        # Test resetting the chess game
        chess.turn = {"black": 1, "white": 0}
        chess.piece_location["e"][4][0] = "white_queen"
        chess.reset()
        self.assertEqual(chess.turn, {"black": 0, "white": 1})
        self.assertEqual(chess.piece_location["e"][4][0], "")


if __name__ == "__main__":
    unittest.main()
