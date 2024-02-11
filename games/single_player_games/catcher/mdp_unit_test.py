import json
import importlib
import unittest
import pygame
import sys

if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
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


class TestCatcherGame(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_handle_events_catcher_movement(self):
        self.test_number = 1

        game = Game()
        # Mocking event to simulate left key press
        original_x = game.state_manager.catcher_position_x
        left_key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})
        game.run(left_key_event)
        self.assertTrue(
            original_x > game.state_manager.catcher_position_x
        )

        # Mocking event to simulate right key press
        original_x = game.state_manager.catcher_position_x
        right_key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT})
        game.run(right_key_event)
        self.assertTrue(
            original_x <  game.state_manager.catcher_position_x
        )

    def test_ball_update(self):
        self.test_number = 3

        game = Game()
        self.assertTrue(len(game.state_manager.balls) > 0)
        for ball in game.state_manager.balls:
            initial_position_y = ball["y"]
            game.run(pygame.event.Event(pygame.NOEVENT))
            self.assertTrue(game.state_manager.balls[0]["y"] > initial_position_y)

    def test_collision_score_update(self):
        self.test_number = 4

        game = Game()
        game.state_manager.game_over = False
        game.state_manager.score = 0
        game.state_manager.balls[0]["x"] = game.state_manager.catcher_position_x
        game.state_manager.balls[0]["y"] = game.state_manager.catcher_position_y
        # pygame.NOEVENT
        game.run(pygame.event.Event(pygame.NOEVENT))
        game.run(pygame.event.Event(pygame.NOEVENT))
        self.assertEqual(game.state_manager.score, 1)

    def test_game_over(self):
        self.test_number = 6

        # Mocking event to simulate right key press
        game = Game()
        game.state_manager.score = 10
        game.state_manager.game_over = True
        original_x = game.state_manager.catcher_position_x
        right_key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT})
        game.run(right_key_event)
        #game.run(right_key_event)
        self.assertEqual(original_x, game.state_manager.catcher_position_x)

        game = Game()
        game.state_manager.score = 10
        game.state_manager.game_over = True
        left_key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})
        game.run(left_key_event)
        self.assertEqual(original_x, game.state_manager.catcher_position_x)


if __name__ == "__main__":
    unittest.main(testRunner=JsonTestRunner(verbosity=2))