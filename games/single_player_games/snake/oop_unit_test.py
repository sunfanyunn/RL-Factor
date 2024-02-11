import unittest
from unittest.mock import patch, Mock
import pygame
import importlib
import sys
# sys.path.append("..")
# from utils import JsonTestRunner, JsonTestResult
import json
# sys.path.pop()
#from decorators import category

if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    spec = importlib.util.spec_from_file_location("oop", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)
    if hasattr(game_module, "SnakeGame"):
        SnakeGame = game_module.SnakeGame
        Snake = game_module.Snake
        Food = game_module.Food
        GRID_WIDTH = game_module.GRID_WIDTH
        GRID_HEIGHT = game_module.GRID_HEIGHT
    else:
        SnakeGame = game_module.Game
        Snake = game_module.Snake
        Food = game_module.Food
        GRID_WIDTH = game_module.GRID_WIDTH
        GRID_HEIGHT = game_module.GRID_HEIGHT
else:
    from oop import SnakeGame, Snake, Food, GRID_WIDTH, GRID_HEIGHT


# Set up a mock display for Pygame
pygame.display.set_mode((1, 1))


import unittest
class JsonTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        test_name = test._testMethodName
        test_number = getattr(test, "test_number", None)
        self.test_results.append(
            {"function_name": test_name, "test_number": test_number, "status": "OK"}
        )

    def addError(self, test, err):
        super().addError(test, err)
        test_name = test._testMethodName
        test_number = getattr(test, "test_number", None)
        self.test_results.append(
            {
                "function_name": test_name,
                "test_number": test_number,
                "message": str(err),
                "status": "ERROR",
            }
        )

    def addFailure(self, test, err):
        super().addFailure(test, err)
        test_name = test._testMethodName
        test_number = getattr(test, "test_number", None)
        self.test_results.append(
            {
                "function_name": test_name,
                "test_number": test_number,
                "message": str(err),
                "status": "FAIL",
            }
        )


class JsonTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resultclass = JsonTestResult

    def run(self, test):
        result = super().run(test)
        with open("test_results.json", "w") as f:
            json.dump(result.test_results, f, indent=4)
        return result


class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        self.game = SnakeGame()
        if hasattr(self.game, "eel"):
            self.game.snake = self.game.eel

    def test_reset_game(self):
        # Test whether the game can be reset correctly
        self.game.game_over = True
        self.game.reset_game()
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.win_message)
        self.assertEqual(len(self.game.snake.body), 1)

    def test_snake_collision_with_wall(self):
        # Test snake collision with the wall
        self.game.snake.rect.x = -1  # Simulate collision with the left wall
        self.assertTrue(self.game.snake.check_collision())

    def test_snake_collision_with_self(self):
        # Test snake collision with itself
        self.game.snake.body = [
            (0, 0),
            (20, 0),
            (20, 20),
            (0, 20),
            (0, 0),
        ]  # Create a circular body
        self.assertTrue(self.game.snake.check_collision())

    def test_snake_grow(self):
        # Test snake growing when colliding with food
        initial_length = len(self.game.snake.body)
        self.game.snake.rect.topleft = (
            self.game.food.rect.topleft
        )  # Set snake position to food
        self.game.snake.update()  # Update game state to simulate collision with food
        self.assertEqual(len(self.game.snake.body), initial_length + 1)

    def test_food_randomize_position(self):
        # Test whether food randomizes its position within the grid
        initial_position = self.game.food.rect.topleft
        self.game.food.randomize_position()
        new_position = self.game.food.rect.topleft
        self.assertNotEqual(initial_position, new_position)

    def test_snake_direction_change(self):
        # Test snake direction change
        self.game.snake.direction = "RIGHT"
        self.game.snake.change_direction("LEFT")  # Should not change to the left
        self.assertEqual(
            self.game.snake.direction, "RIGHT"
        )  # Direction should remain "RIGHT"

    def test_snake_direction_change_valid(self):
        # Test valid snake direction change
        self.game.snake.direction = "RIGHT"
        self.game.snake.change_direction("UP")  # Should change to "UP"
        self.assertEqual(self.game.snake.direction, "UP")


if __name__ == "__main__":
    unittest.main(testRunner=JsonTestRunner(verbosity=2))

