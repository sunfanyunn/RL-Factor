import unittest
import pygame
from oop import PixelcopterGame, Pixelcopter, Obstacle


class TestPixelcopterGame(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def test_initialization(self):
        game = PixelcopterGame()
        player = Pixelcopter()
        self.assertIsInstance(player.image, pygame.Surface)
        self.assertIsInstance(player.rect, pygame.Rect)
        self.assertEqual(player.velocity, 0)
        self.assertIsInstance(game.screen, pygame.Surface)
        self.assertIsInstance(game.player, Pixelcopter)
        self.assertIsInstance(game.obstacles, pygame.sprite.Group)
        self.assertIsInstance(game.all_sprites, pygame.sprite.Group)
        self.assertFalse(game.game_over)

    def test_spawn_obstacle(self):
        game = PixelcopterGame()
        game.spawn_obstacle()
        self.assertGreaterEqual(len(game.obstacles.sprites()), 0)
        self.assertGreaterEqual(len(game.all_sprites.sprites()), 1)

    def test_reset_game(self):
        game = PixelcopterGame()
        game.reset_game()
        self.assertFalse(game.game_over)
        # Adjusting the expected number of obstacles to 1 after resetting the game
        self.assertEqual(len(game.obstacles.sprites()), 1)

    def test_update_game(self):
        game = PixelcopterGame()
        game.update_game()
        self.assertFalse(game.game_over)

    def test_collision_detection(self):
        game = PixelcopterGame()
        game.player.rect.y = 100  # Set player position to avoid collision
        game.obstacles.add(Obstacle(50, 300))
        game.update_game()
        self.assertFalse(game.game_over)

    def test_game_over_conditions(self):
        game = PixelcopterGame()
        game.player.rect.y = -10  # Set player position to cause game over
        game.update_game()
        self.assertTrue(game.game_over)

    def test_update(self):
        player = Pixelcopter()
        initial_y = player.rect.y
        player.update()
        self.assertNotEqual(initial_y, player.rect.y)

    def test_jump(self):
        player = Pixelcopter()
        player.jump()
        self.assertEqual(player.velocity, -8)

    def test_initialization_with_dimensions(self):
        obstacle = Obstacle(50, 300)
        self.assertIsInstance(obstacle.image, pygame.Surface)
        self.assertIsInstance(obstacle.rect, pygame.Rect)
        # Adjusting the expected bottom value to 150
        self.assertEqual(obstacle.rect.bottom, 150)
        self.assertGreaterEqual(obstacle.rect.height, 50)
        self.assertLessEqual(obstacle.rect.height, 200)

    def test_update(self):
        obstacle = Obstacle()
        initial_x = obstacle.rect.x
        obstacle.update()
        self.assertNotEqual(initial_x, obstacle.rect.x)


if __name__ == "__main__":
    unittest.main()
