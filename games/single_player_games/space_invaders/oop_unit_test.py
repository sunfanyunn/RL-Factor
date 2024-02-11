import unittest
import pygame
from unittest.mock import Mock


from oop import (
    SpaceInvadersGame,
    Player,
    Enemy,
    Bullet,
    WIDTH,
    HEIGHT,
    PLAYER_SIZE,
    PLAYER_SPEED,
    ENEMY_SIZE,
    ENEMY_SPEED,
    ENEMY_ROWS,
    ENEMY_COLS,
)


class TestSpaceInvadersGame(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def test_create_enemies(self):
        game = SpaceInvadersGame()
        self.assertEqual(len(game.enemies), ENEMY_ROWS * ENEMY_COLS)

    def test_player_movement(self):
        player = Player()
        initial_position = player.rect.center

        # Simulate pressing the left arrow key
        pygame.key.get_pressed = Mock(
            return_value={pygame.K_LEFT: True, pygame.K_RIGHT: False}
        )
        player.update()
        self.assertEqual(player.rect.centerx, initial_position[0] - PLAYER_SPEED)
        # Simulate pressing the right arrow key
        pygame.key.get_pressed = Mock(
            return_value={pygame.K_LEFT: False, pygame.K_RIGHT: True}
        )

        player.update()

        self.assertEqual(player.rect.centerx, initial_position[0])

    def test_enemy_movement(self):
        enemy = Enemy(0, 0)
        initial_position = enemy.rect.topleft

        enemy.update()
        self.assertEqual(
            enemy.rect.topleft,
            (initial_position[0] + ENEMY_SPEED * enemy.direction, initial_position[1]),
        )

    def test_bullet_update(self):
        bullet = Bullet(100, 100)
        initial_position = bullet.rect.bottom

        bullet.update()
        self.assertEqual(bullet.rect.bottom, initial_position - 5)

    def test_enemy_reached_edge(self):
        enemy = Enemy(1, 1)
        self.assertFalse(enemy.reached_edge())

        enemy.rect.left = -1
        self.assertTrue(enemy.reached_edge())

        enemy.rect.right = WIDTH + 1
        self.assertTrue(enemy.reached_edge())

    def test_enemy_change_direction(self):
        enemy = Enemy(0, 0)
        initial_direction = enemy.direction

        enemy.change_direction()
        self.assertEqual(enemy.direction, initial_direction * -1)


if __name__ == "__main__":
    unittest.main()
