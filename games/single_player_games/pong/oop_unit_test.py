import unittest
import pygame
from pygame.locals import QUIT, KEYDOWN, K_r
from unittest.mock import patch

# Import the classes from the provided code
from oop import PongGame, Ball, PaddleHuman, PaddleCPU, WIDTH, HEIGHT, BLACK, WHITE


class TestPongGame(unittest.TestCase):
    def setUp(self):
        self.game = PongGame()

    def test_reset_round(self):
        self.game.reset_round()
        self.assertEqual(self.game.ball.rect.topleft, (WIDTH // 2, HEIGHT // 2))
        self.assertEqual(self.game.paddle_human.rect.topleft, (10, HEIGHT // 2 - 50))
        self.assertEqual(
            self.game.paddle_cpu.rect.topleft, (WIDTH - 30, HEIGHT // 2 - 50)
        )

    def test_reset_game(self):
        self.game.reset_game()
        self.assertEqual(self.game.score_human, 0)
        self.assertEqual(self.game.score_cpu, 0)
        self.assertFalse(self.game.game_over)

    def test_ball_reset(self):
        ball = Ball()
        ball.reset()
        self.assertEqual(ball.rect.topleft, (WIDTH // 2, HEIGHT // 2))
        self.assertEqual(ball.speed, [5, 5])

    def test_ball_update(self):
        ball = Ball()
        ball.rect.topleft = (10, 10)
        ball.speed = [2, 2]
        ball.update()
        self.assertEqual(ball.rect.topleft, (12, 12))
        ball.speed = [-2, -2]
        ball.update()
        self.assertEqual(ball.rect.topleft, (10, 10))

    def test_paddle_human_reset(self):
        paddle_human = PaddleHuman()
        paddle_human.reset()
        self.assertEqual(paddle_human.rect.topleft, (10, HEIGHT // 2 - 50))

    def test_paddle_human_update(self):
        paddle_human = PaddleHuman()
        paddle_human.rect.topleft = (10, 10)
        keys = {pygame.K_UP: False, pygame.K_DOWN: False}

        with patch("pygame.key.get_pressed", return_value=keys):
            paddle_human.update()
        self.assertEqual(paddle_human.rect.topleft, (10, 10))

        keys[pygame.K_UP] = True
        with patch("pygame.key.get_pressed", return_value=keys):
            paddle_human.update()
        self.assertEqual(
            paddle_human.rect.topleft, (10, 10 - paddle_human.speed)
        )  # Update this line

        keys[pygame.K_UP] = False
        keys[pygame.K_DOWN] = True
        with patch("pygame.key.get_pressed", return_value=keys):
            paddle_human.update()
        self.assertEqual(paddle_human.rect.topleft, (10, 10))

    def test_paddle_cpu_reset(self):
        paddle_cpu = PaddleCPU()
        paddle_cpu.reset()
        self.assertEqual(paddle_cpu.rect.topleft, (WIDTH - 30, HEIGHT // 2 - 50))

    def test_handle_events_quit(self):
        with patch("pygame.event.get", return_value=[pygame.event.Event(QUIT)]):
            with self.assertRaises(SystemExit):
                self.game.handle_events()

    def test_handle_events_restart(self):
        with patch(
            "pygame.event.get", return_value=[pygame.event.Event(KEYDOWN, key=K_r)]
        ):
            self.game.game_over = True
            self.game.handle_events()
            self.assertFalse(self.game.game_over)


if __name__ == "__main__":
    unittest.main()
