import unittest
import sys
from unittest.mock import patch
import importlib

sys.path.append("../")
from decorators import category

if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    spec = importlib.util.spec_from_file_location("game", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)
    if hasattr(game_module, "TicTacToeGame"):
        TicTacToeGame = game_module.TicTacToeGame
    else:
        TicTacToeGame = game_module.Game
else:
    from oop import (
        TicTacToeGame,
    )  # Default to the standard implementation if no argument is provided


class Test(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToeGame()
        self.game.init_assets()

    def test_initial_state(self):
        self.assertEqual(self.game.current_player, "X")
        self.assertFalse(self.game.game_over)
        for row in self.game.board:
            self.assertEqual(row, ["", "", ""])

    def test_player_turn_switching(self):
        self.game.current_player = "X"

        # Simulate a mouse click
        self.game.handle_click(
            (100, 100)
        )  # You need to implement this method to handle mouse events

        self.assertEqual(self.game.current_player, "O")

        # Simulate another mouse click
        self.game.handle_click((200, 100))

        self.assertEqual(self.game.current_player, "X")

    # def test_valid_move(self):
    #     self.assertTrue(self.game.is_valid_move(0, 0))
    #     self.assertTrue(self.game.is_valid_move(2, 1))
    #     self.game.make_move(0, 0)
    #     self.assertFalse(self.game.is_valid_move(0, 0))

    def test_win_conditions(self):
        self.game.board = [["X", "X", "X"], ["", "", ""], ["", "", ""]]
        self.assertEqual(self.game.check_win(), "X")

        self.game.board = [["O", "X", ""], ["O", "X", ""], ["O", "", ""]]
        self.assertEqual(self.game.check_win(), "O")

        self.game.board = [["X", "", ""], ["", "X", ""], ["", "", "X"]]
        self.assertEqual(self.game.check_win(), "X")

        self.game.board = [["X", "O", "X"], ["O", "X", "X"], ["X", "X", "O"]]
        self.assertEqual(self.game.check_win(), "X")

    def test_draw_condition(self):
        self.game.board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        self.assertNotEqual(self.game.check_win(), "X")
        self.assertNotEqual(self.game.check_win(), "O")

    def test_game_reset(self):
        self.game.board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        self.game.current_player = "O"
        self.game.reset_game()
        self.assertEqual(self.game.current_player, "X")
        self.assertFalse(self.game.game_over)
        for row in self.game.board:
            self.assertEqual(row, ["", "", ""])


if __name__ == "__main__":
    unittest.main(verbosity=2)
