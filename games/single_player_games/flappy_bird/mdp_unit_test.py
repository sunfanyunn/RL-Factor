import json
import importlib
import unittest
import pygame
from mdp import Game
import sys
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"


if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    print(implementation_path)
    spec = importlib.util.spec_from_file_location("", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)

    Game = game_module.Game
else:
    from mdp import Game

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


class Test(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_bird_flap(self):
        self.test_number = 2

        game = Game()
        initial_y = game.state_manager.bird_position_y
        game.run(event=pygame.event.Event(pygame.NOEVENT))
        game.run(event=pygame.event.Event(pygame.NOEVENT))
        game.run(event=pygame.event.Event(pygame.NOEVENT))
        new_y = game.state_manager.bird_position_y
        self.assertTrue(new_y > initial_y)

        initial_y = game.state_manager.bird_position_y
        mouse_click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1})
        game.run(event=mouse_click_event)
        game.run(event=pygame.event.Event(pygame.NOEVENT))
        game.run(event=pygame.event.Event(pygame.NOEVENT))
        new_y_with_flap = game.state_manager.bird_position_y
        self.assertTrue(new_y > new_y_with_flap)

    def test_pipe_logic(self):
        self.test_number = 3

        game = Game()
        initial_pipe_positions = [pipe["x"] for pipe in game.state_manager.pipe_positions]
        game.game_over = False
        game.run(event=pygame.event.Event(pygame.NOEVENT))
        new_pipe_positions = [pipe["x"] for pipe in game.state_manager.pipe_positions]
        for initial, new in zip(initial_pipe_positions, new_pipe_positions):
            self.assertTrue(new < initial)

    def test_collision(self):
        self.test_number = 4

        game = Game()
        game.state_manager.pipe_positions = [
            {
                "x": game.state_manager.bird_position_x,
                "height": game.state_manager.SCREEN_HEIGHT,
            }
        ]
        # set tothe same location
        game.run(event=pygame.event.Event(pygame.NOEVENT))  # Update the game state
        self.assertTrue(game.state_manager.game_over)

        game = Game()
        game.state_manager.bird_position_y = game.state_manager.SCREEN_HEIGHT + 0.1  # Move the bird below the screen
        game.run(event=pygame.event.Event(pygame.NOEVENT))  # Update the game state
        self.assertTrue(game.state_manager.game_over)

    def test_bird_passes_pipe(self):
        self.test_number = 6

        game = Game()
        PIPE_WIDTH = game.state_manager.PIPE_WIDTH
        pipe = game.state_manager.pipe_positions[0]
        self.assertTrue(game.state_manager.score == 0)

        game.state_manager.bird_position_x = pipe["x"] - PIPE_WIDTH + 1
        game.run(event=pygame.event.Event(pygame.NOEVENT))  # Update the game state
        # Move the bird to the right of the pipe to simulate passing it
        game.state_manager.bird_position_x = pipe["x"] + PIPE_WIDTH + 1
        game.run(event=pygame.event.Event(pygame.NOEVENT))  # Update the game state
        self.assertTrue(game.state_manager.score > 0)


if __name__ == "__main__":
    unittest.main(testRunner=JsonTestRunner(verbosity=2))
