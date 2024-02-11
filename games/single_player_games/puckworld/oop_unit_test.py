import unittest
import pygame
from oop import PuckWorld, Agent, GreenDot, RedPuck, WIDTH, HEIGHT, FPS


class TestPuckWorld(unittest.TestCase):
    def setUp(self):
        self.game = PuckWorld()

    def test_agent_thruster(self):
        keys = [0] * 323  # An array with all keys set to 0
        keys[pygame.K_UP] = 1
        self.game.agent.apply_thrusters(keys)
        self.assertEqual(self.game.agent.velocity, [0, -1])

    def test_agent_update(self):
        self.game.agent.rect.topleft = (0, 0)
        self.game.agent.velocity = [1, 1]
        self.game.agent.update()
        self.assertEqual(self.game.agent.rect.topleft, (1, 1))

    def test_agent_velocity_decay(self):
        self.game.agent.velocity = [2, 2]
        self.game.agent.update()
        self.assertEqual(self.game.agent.velocity, [1.96, 1.96])

    def test_green_dot_randomize_position(self):
        initial_position = self.game.green_dot.rect.topleft
        self.game.green_dot.randomize_position()
        self.assertNotEqual(self.game.green_dot.rect.topleft, initial_position)

    def test_red_puck_update(self):
        initial_position = self.game.red_puck.rect.topleft
        self.game.red_puck.update(self.game.agent)
        self.assertNotEqual(self.game.red_puck.rect.topleft, initial_position)

    def test_collision_with_green_dot(self):
        self.game.agent.rect.topleft = self.game.green_dot.rect.topleft
        initial_position = self.game.green_dot.rect.topleft
        self.game.update_game()
        self.assertNotEqual(self.game.green_dot.rect.topleft, initial_position)

    def test_collision_with_red_puck(self):
        self.game.agent.rect.topleft = self.game.red_puck.rect.topleft
        self.game.update_game()
        self.assertTrue(self.game.game_over)


if __name__ == "__main__":
    unittest.main()
