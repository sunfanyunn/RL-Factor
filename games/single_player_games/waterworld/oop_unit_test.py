import unittest
import pygame
from oop import WaterWorldGame, Agent, Circle, GRID_SIZE, GREEN, RED


class TestWaterWorldGame(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        game = WaterWorldGame()
        self.assertIsInstance(game, WaterWorldGame)

    def test_reset_game(self):
        game = WaterWorldGame()
        game.reset_game()
        self.assertFalse(game.game_over)
        self.assertFalse(game.win_message)
        self.assertEqual(game.score, 0)
        self.assertTrue(game.all_sprites)
        self.assertTrue(game.circles)

    def test_spawn_circle(self):
        game = WaterWorldGame()
        initial_circle_count = len(game.circles.sprites())
        game.spawn_circle(GREEN)
        self.assertEqual(len(game.circles.sprites()), initial_circle_count + 1)

    def test_agent_movement(self):
        agent = Agent()
        initial_position = agent.rect.topleft
        agent.move("RIGHT")
        self.assertEqual(
            agent.rect.topleft,
            (initial_position[0] + agent.rect.width, initial_position[1]),
        )

    def test_circle_reset(self):
        circle = Circle(GREEN)
        initial_position = circle.rect.topleft
        circle.reset()
        self.assertNotEqual(circle.rect.topleft, initial_position)

    def test_update_circles(self):
        game = WaterWorldGame()
        initial_score = game.score
        game.circles.empty()

        initial_circle_count = len(game.circles.sprites())

        game.spawn_circle(GREEN)
        # Assume the agent collides with a green circle
        green_circle = game.circles.sprites()[0]
        game.agent.rect.topleft = green_circle.rect.topleft
        initial_green_count = sum(
            circle.color == GREEN for circle in game.circles.sprites()
        )
        game.update_circles()
        self.assertEqual(game.score, initial_score + 1)

        game.circles.empty()
        game.spawn_circle(RED)
        red_circle = game.circles.sprites()[0]

        # Assume the agent collides with the red circle
        game.agent.rect.topleft = red_circle.rect.topleft
        initial_red_count = sum(
            circle.color == RED for circle in game.circles.sprites()
        )
        game.update_circles()
        self.assertEqual(game.score, initial_score)

    def test_handle_events(self):
        game = WaterWorldGame()
        initial_agent_x = game.agent.rect.x

        # Test handling events when the game is not over
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT}))
        game.handle_events()
        self.assertEqual(game.agent.rect.x, initial_agent_x + GRID_SIZE)


if __name__ == "__main__":
    unittest.main()
