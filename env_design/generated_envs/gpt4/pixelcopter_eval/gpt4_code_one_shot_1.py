import pygame
import sys
import random

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CAVERN_WIDTH = 100  # Width of the gap in the cavern
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_WIDTH = 50
OBSTACLE_SPEED = 3
OBSTACLE_GAP_SIZE = 200
OBSTACLE_FREQUENCY = 60


class Game:
    def __init__(self):
        # Initializing the display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pixelcopter Game")

        # Creating Clock
        self.clock = pygame.time.Clock()
        self.game_over = False

        # Creating Sprite Groups
        self.player = Pixelcopter()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Scoring
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

        self.obstacle_timer = 0

    # Other methods will go here

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
