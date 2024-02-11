import unittest
import pygame
from unittest.mock import patch
import sys

sys.path.append("../")
from decorators import category
import importlib


if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    spec = importlib.util.spec_from_file_location("game", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)

    if hasattr(game_module, "Game_2048"):
        Game_2048 = game_module.Game_2048

    else:
        Game_2048 = game_module.Game

else:
    from game import Game_2048


class TestGame2048(unittest.TestCase):
    def setUp(self):
        self.game = Game_2048()

    @category("Init")
    def test_init_board(self):
        # Test if the board is initialized properly
        board = self.game.init_board()
        self.assertEqual(len(board), 4)
        for row in board:
            self.assertEqual(len(row), 4)

    @category("Mechanics")
    def test_add_new_num(self):
        # Test if numbers are added to the board correctly
        board = self.game.init_board()
        self.game.add_new_num(2)
        num_count = sum(row.count("0") for row in board)
        self.assertEqual(num_count, 12)  # 2 new numbers were added

    @category("Mechanics")
    def test_check_win(self):
        # Test if the game win condition is checked correctly
        board = [
            ["2", "4", "8", "16"],
            ["32", "64", "128", "256"],
            ["512", "1024", "2048", "4096"],
            ["8192", "16384", "32768", "65536"],
        ]
        self.game.board = board
        self.assertTrue(self.game.check_win())

    @category("Movement")
    def test_main(self):
        # Test the main game logic for moving and merging values
        board = [
            ["2", "4", "8", "16"],
            ["2", "4", "8", "16"],
            ["2", "4", "8", "16"],
            ["2", "4", "8", "16"],
        ]
        self.game.board = board

        # Test moving up
        self.game.main("u")
        expected_board = [
            ["4", "8", "16", "32"],
            ["4", "8", "16", "32"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
        ]
        self.assertEqual(self.game.board[0], expected_board[0])

        # # Test merging and moving right
        # self.game.main('r')
        # expected_board = [['0', '0', '4', '8'],
        #                   ['0', '0', '4', '8'],
        #                   ['0', '0', '0', '0'],
        #                   ['0', '0', '0', '2']]
        # self.assertEqual(self.game.board, expected_board)

    @category("Movement")
    def test_can_move(self):
        # Test if the can_move method correctly identifies whether moves are possible
        board = [
            ["2", "4", "8", "16"],
            ["32", "64", "128", "256"],
            ["512", "1024", "2048", "4096"],
            ["8192", "16384", "32768", "65536"],
        ]
        self.game.board = board
        self.assertFalse(self.game.can_move())

        board = [
            ["2", "4", "8", "16"],
            ["32", "64", "128", "256"],
            ["512", "1024", "2048", "0"],
            ["8192", "16384", "32768", "65536"],
        ]
        self.game.board = board
        self.assertTrue(self.game.can_move())

    @category("Mechanics")
    def test_check_lose(self):
        # Test if the game loss condition is checked correctly
        board = [
            ["2", "4", "8", "16"],
            ["32", "64", "128", "256"],
            ["2", "4", "8", "16"],
            ["32", "256", "128", "64"],
        ]
        self.game.board = board
        self.assertTrue(self.game.check_lose())

    @category("Mechanics")
    def test_update_score(self):
        # Test if the score is updated correctly
        self.game.update_score(10)
        self.assertEqual(self.game.score, 10)

    @category("Reset")
    def test_reset(self):
        # Test if the game can be reset
        self.game.score = 100
        self.game.reset()
        self.assertEqual(self.game.score, 0)


if __name__ == "__main__":
    unittest.main()
