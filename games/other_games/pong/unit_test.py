import unittest
from unittest.mock import patch, Mock
import pygame
import importlib
import sys

sys.path.append("../")
from decorators import category

if len(sys.argv) > 1:
    # Pop the last argument from sys.argv, which is the path to the game implementation
    implementation_path = sys.argv.pop()
    spec = importlib.util.spec_from_file_location("game", implementation_path)
    game_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_module)
    if hasattr(game_module, "PongGame"):
        PongGame = game_module.PongGame
    else:
        PongGame = game_module.Game
    Ball = game_module.Ball
    Paddle = game_module.Paddle
    PADDLE_SPEED = game_module.PADDLE_SPEED
    BALL_SPEED = game_module.BALL_SPEED
    SCREEN_HEIGHT = game_module.SCREEN_HEIGHT
    SCREEN_WIDTH = game_module.SCREEN_WIDTH
    PADDLE_DIMS = game_module.PADDLE_DIMS
    BALL_RADIUS = game_module.BALL_RADIUS
else:
    try:
        from game import (
            PongGame,
            Ball,
            Paddle,
            PADDLE_SPEED,
            BALL_SPEED,
            SCREEN_HEIGHT,
            SCREEN_WIDTH,
            PADDLE_DIMS,
            BALL_RADIUS,
        )
    except Exception as e:
        print(e)


class Test(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = PongGame()
        self.ball = Ball()

    @category("Init")
    def test_init_assets(self):
        self.game.init_assets()
        self.assertEqual(self.game.left_score, 0)
        self.assertEqual(self.game.right_score, 0)
        self.assertTrue(self.game.ball_sprite)
        self.assertTrue(self.game.left_paddle_sprite)
        self.assertTrue(self.game.right_paddle_sprite)

    @category("Movement")
    @patch("pygame.key.get_pressed")
    def test_movePaddles_up(self, mock_get_pressed):
        self.game.init_assets()
        all_keys = {
            self.game.left_paddle_sprite.up_key: True,
            self.game.left_paddle_sprite.down_key: False,
            self.game.right_paddle_sprite.up_key: True,
            self.game.right_paddle_sprite.down_key: False,
        }
        mock_get_pressed.return_value = all_keys
        prev_left_paddle_y = self.game.left_paddle_sprite.rect.y
        prev_right_paddle_y = self.game.right_paddle_sprite.rect.y

        self.game.paddles.update()

        self.assertEqual(
            self.game.left_paddle_sprite.rect.y, prev_left_paddle_y - PADDLE_SPEED
        )
        self.assertEqual(
            self.game.right_paddle_sprite.rect.y, prev_right_paddle_y - PADDLE_SPEED
        )

    @category("Movement")
    @patch("pygame.key.get_pressed")
    def test_movePaddles_down(self, mock_get_pressed):
        self.game.init_assets()
        all_keys = {
            self.game.left_paddle_sprite.up_key: False,
            self.game.left_paddle_sprite.down_key: True,
            self.game.right_paddle_sprite.up_key: False,
            self.game.right_paddle_sprite.down_key: True,
        }
        mock_get_pressed.return_value = all_keys
        prev_left_paddle_y = self.game.left_paddle_sprite.rect.y
        prev_right_paddle_y = self.game.right_paddle_sprite.rect.y

        self.game.paddles.update()

        self.assertEqual(
            self.game.left_paddle_sprite.rect.y, prev_left_paddle_y + PADDLE_SPEED
        )
        self.assertEqual(
            self.game.right_paddle_sprite.rect.y, prev_right_paddle_y + PADDLE_SPEED
        )

    @category("Collision")
    def test_moveBall_top_wall(self):
        original_ball_speed = list(BALL_SPEED)
        self.game.init_assets()
        self.game.ball_sprite.rect.top = 0
        self.game.ball_sprite.update()
        self.assertEqual(BALL_SPEED[1], -original_ball_speed[1])

    @category("Collision")
    def test_moveBall_bottom_wall(self):
        original_ball_speed = list(BALL_SPEED)
        self.game.init_assets()
        self.game.ball_sprite.rect.bottom = SCREEN_HEIGHT
        self.game.ball_sprite.update()
        self.assertEqual(BALL_SPEED[1], -original_ball_speed[1])

    @category("Collision")
    @patch.object(Ball, "reset_ball")
    def test_moveBall_out_left(self, mock_reset_ball):
        self.game.init_assets()
        self.game.ball_sprite.rect.left = -10
        self.game.ball_sprite.update()
        mock_reset_ball.assert_called_once()
        self.assertEqual(self.game.right_score, 1)
        self.assertEqual(self.game.left_score, 0)

    @category("Collision")
    @patch.object(Ball, "reset_ball")
    def test_moveBall_out_right(self, mock_reset_ball):
        self.game.init_assets()
        self.game.ball_sprite.rect.right = SCREEN_WIDTH + 10
        self.game.ball_sprite.update()
        mock_reset_ball.assert_called_once()
        self.assertEqual(self.game.right_score, 0)
        self.assertEqual(self.game.left_score, 1)

    # def test_moveBall_collides_left_paddle(self):
    #     original_ball_speed = list(BALL_SPEED)
    #     self.game.init_assets()
    #     self.game.ball_sprite.rect.left = PADDLE_DIMS[0] - 1
    #     self.game.ball_sprite.update()
    #     self.assertEqual(BALL_SPEED[0], -original_ball_speed[0])

    @category("Collision")
    def test_moveBall_collides_right_paddle(self):
        original_ball_speed = list(BALL_SPEED)
        self.game.init_assets()
        self.game.ball_sprite.rect.right = SCREEN_WIDTH - PADDLE_DIMS[0] + 1
        self.game.ball_sprite.update()
        self.assertEqual(BALL_SPEED[0], -original_ball_speed[0])

    @category("Reset")
    def test_reset_game_called(self):
        mock_event = Mock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        self.game.init_assets = Mock()

    @category("Reset")
    def test_reset_ball_position(self):
        self.game.ball_sprite.reset_ball()
        expected_x = SCREEN_WIDTH // 2 - BALL_RADIUS
        expected_y = SCREEN_HEIGHT // 2 - BALL_RADIUS
        self.assertEqual(self.game.ball_sprite.rect.x, expected_x)
        self.assertEqual(self.game.ball_sprite.rect.y, expected_y)

    @category("Mechanics")
    def test_reset_ball_speed_inversion(self):
        initial_speed = list(BALL_SPEED)
        self.game.ball_sprite.reset_ball()
        self.assertEqual(BALL_SPEED[0], -initial_speed[0])

    @category("Reset")
    @patch.object(PongGame, "init_assets")
    def test_reset_game(self, mock_init_assets):
        mock_event = Mock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.pos = (self.game.reset_button.x, self.game.reset_button.y)
        self.game.reset_game(mock_event)
        mock_init_assets.assert_called_once()

    # @patch('pygame.mouse.get_pos')
    # def test_render_game_button_highlight(self, mock_get_pos):
    #     mock_get_pos.return_value = (self.game.reset_button.x, self.game.reset_button.y)
    #     mock_draw_rect = Mock()
    #     with patch('pygame.draw.rect', mock_draw_rect):
    #         self.game.render_game()
    #     mock_draw_rect.assert_called_with(self.game.screen, HIGHLIGHT_COLOR, self.game.reset_button)


if __name__ == "__main__":
    unittest.main(verbosity=2)
