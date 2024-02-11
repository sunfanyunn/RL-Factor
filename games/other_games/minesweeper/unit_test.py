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
    if hasattr(game_module, "Minesweeper"):
        Minesweeper = game_module.Minesweeper
        BOMB = game_module.BOMB
        EMPTY = game_module.EMPTY
        NUM_BOMBS = game_module.NUM_BOMBS
    else:
        Minesweeper = game_module.Game
        BOMB = game_module.HAZARD
        EMPTY = game_module.EMPTY
        NUM_BOMBS = game_module.NUM_HAZARDS

else:
    from game import Minesweeper, BOMB, EMPTY, NUM_BOMBS


class Test(unittest.TestCase):
    def setUp(self):
        self.game = Minesweeper()

    @category("Init")
    def test_init_assets(self):
        self.game.init_assets()
        bomb_count = sum([row.count(BOMB) for row in self.game.board])
        self.assertEqual(bomb_count, NUM_BOMBS)
        for row in self.game.revealed:
            for cell in row:
                self.assertFalse(cell)

    @category("Mechanics")
    def test_placeBombs(self):
        self.game.init_assets()
        bomb_count = sum([row.count(BOMB) for row in self.game.board])
        self.assertEqual(bomb_count, NUM_BOMBS)

    @category("Mechanics")
    def test_revealCell_with_bomb(self):
        self.game.init_assets()
        self.game.board[1][1] = BOMB
        self.game.reveal_cell(1, 1)
        self.assertTrue(self.game.game_over)
        self.assertTrue(self.game.revealed[1][1])

    @category("Mechanics")
    def test_revealCell_empty_cell(self):
        self.game.init_assets()
        self.game.board[1][1] = EMPTY
        self.game.reveal_cell(1, 1)
        self.assertFalse(self.game.game_over)
        self.assertTrue(self.game.revealed[1][1])

    @category("Mechanics")
    def test_surroundingBombsCount(self):
        self.game.init_assets()
        self.game.board = [
            [EMPTY, BOMB, EMPTY],
            [BOMB, EMPTY, BOMB],
            [EMPTY, BOMB, EMPTY],
        ]
        count = self.game.surrounding_count(1, 1)
        self.assertEqual(count, 4)

    @category("Mechanics")
    def test_check_win_true(self):
        self.game = Minesweeper(3, 3, 2)
        self.game.init_assets()
        self.game.board = [
            [BOMB, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, BOMB],
        ]
        self.game.revealed = [
            [False, True, True],
            [True, True, True],
            [True, True, False],
        ]
        self.assertTrue(self.game.check_win())

    @category("Mechanics")
    def test_check_win_false(self):
        self.game = Minesweeper(3, 3, 2)
        self.game.init_assets()
        self.game.board = [
            [BOMB, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, BOMB],
        ]
        self.game.revealed = [
            [False, False, True],
            [True, True, True],
            [True, True, False],
        ]
        self.assertFalse(self.game.check_win())

    @category("Mechanics")
    def test_revealCell_already_revealed(self):
        self.game.init_assets()
        self.game.revealed[1][1] = True
        self.game.reveal_cell(1, 1)
        self.assertFalse(self.game.game_over)

    @category("Mechanics")
    def test_restart_game_after_game_over(self):
        self.game.init_assets()
        self.game.board[1][1] = BOMB
        self.game.reveal_cell(1, 1)
        self.game.init_assets()
        self.assertFalse(self.game.game_over)


if __name__ == "__main__":
    unittest.main(verbosity=2)
