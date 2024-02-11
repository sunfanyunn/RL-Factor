import unittest
from unittest.mock import MagicMock, patch
import pygame
import sys
import importlib
import json
# import a class from the parent directory without sys
# sys.path.append("..")
# from utils import JsonTestRunner, JsonTestResult

# sys.path.pop()


if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    print(implementation_path)
    spec = importlib.util.spec_from_file_location("oop", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)

    if hasattr(game_module, "BreakoutGame"):
        BreakoutGame = game_module.BreakoutGame
        Paddle = game_module.Paddle
        Ball = game_module.Ball
        Brick = game_module.Brick
        GRID_SIZE = game_module.GRID_SIZE
        WIDTH = game_module.WIDTH
        HEIGHT = game_module.HEIGHT
    else:
        BreakoutGame = game_module.Game
        Paddle = game_module.Paddle
        Ball = game_module.Ball
        Brick = game_module.Brick
        GRID_SIZE = game_module.GRID_SIZE
        WIDTH = game_module.WIDTH
        HEIGHT = game_module.HEIGHT

else:
    from oop import BreakoutGame, Paddle, Ball, Brick, GRID_SIZE, WIDTH, HEIGHT
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


class TestBreakoutGame(unittest.TestCase):
    def setUp(self):
        self.game = BreakoutGame()
        self.test_number = None

    def tearDown(self) -> None:
        pygame.quit()

    def test_paddle_move(self):
        self.test_number = 1
        # Test for moving left
        initial_x = self.game.paddle.rect.x
        self.game.paddle.move_left()
        self.assertEqual(
            self.game.paddle.rect.x, max(initial_x - self.game.paddle.speed, 0)
        )

        # Test for moving right
        initial_x = self.game.paddle.rect.x
        self.game.paddle.move_right()
        self.assertEqual(
            self.game.paddle.rect.x,
            min(initial_x + self.game.paddle.speed, WIDTH - GRID_SIZE * 4),
        )

    def test_ball_update(self):
        self.test_number = 3
        # Test for updating the ball's position
        initial_y = self.game.ball.rect.y
        self.game.update()
        self.assertEqual(
            self.game.ball.rect.y, initial_y + self.game.ball.speed * self.game.ball.dy
        )

        # Test for bouncing off the walls
        initial_dx = self.game.ball.dx
        self.game.ball.bounce_x()
        self.assertEqual(self.game.ball.dx, -initial_dx)

        initial_dy = self.game.ball.dy
        self.game.ball.bounce_y()
        self.assertEqual(self.game.ball.dy, -initial_dy)

    def test_brick_init(self):
        self.test_number = 4
        # Test for initializing bricks
        brick = Brick(10, 20)
        self.assertEqual(brick.rect.topleft, (10, 20))

    def test_ball_init(self):
        self.test_number = 2
        # Test for initializing the ball
        ball = Ball()
        self.assertEqual(
            ball.rect.topleft, ((WIDTH - GRID_SIZE) // 2, HEIGHT - GRID_SIZE * 4)
        )

    def test_update_collide(self):
        # Test for ball-paddle, ball-brick, and ball-wall collisions
        self.test_number = 5
        brick_mock = MagicMock()
        brick_mock.rect = pygame.Rect(0, 0, GRID_SIZE * 2, GRID_SIZE)

        # Ball-paddle collision
        self.game.ball.rect.topleft = (
            (WIDTH - GRID_SIZE) // 2,
            HEIGHT - GRID_SIZE * 2,
        )
        self.game.ball.dy = 1  # To make it move down
        self.game.paddle.rect.topleft = (
            (WIDTH - GRID_SIZE * 4) // 2,
            HEIGHT - GRID_SIZE * 2,
        )
        self.game.update()
        self.assertEqual(self.game.ball.dy, -1)

        # Ball-brick collision
        with patch("pygame.sprite.spritecollide", return_value=[brick_mock]):
            self.game.update()
            self.assertEqual(self.game.ball.dy, -1)

        # Ball-wall collision
        self.game.ball.rect.topleft = (0, HEIGHT - GRID_SIZE * 4)
        self.game.ball.dx = -1
        self.game.update()
        self.assertEqual(self.game.ball.dx, 1)

    def test_game_over(self):
        self.test_number = 8
        # Test for game over condition
        self.game.ball.rect.y = HEIGHT
        self.game.update()
        self.assertTrue(self.game.game_over)

    def test_reset_game(self):
        self.test_number = 9
        # Test for resetting the game
        initial_paddle_pos = self.game.paddle.rect.topleft
        initial_ball_pos = self.game.ball.rect.topleft
        initial_bricks = len(self.game.bricks)

        self.game.reset_game()

        # Check if paddle and ball positions are reset
        self.assertEqual(self.game.paddle.rect.topleft, initial_paddle_pos)
        self.assertEqual(self.game.ball.rect.topleft, initial_ball_pos)

        # Check if the number of bricks is the same as before
        self.assertEqual(len(self.game.bricks), initial_bricks)

        # Check if the game is not over after reset
        self.assertFalse(self.game.game_over)


if __name__ == "__main__":
    unittest.main(testRunner=JsonTestRunner(verbosity=2))
