import pygame
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PIPE_WIDTH = 80
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_GAP = 200
GRAVITY = 1
JUMP_HEIGHT = -12
PIPE_MOVEMENT = -5
PIPE_SPAWN_TIME = 1500


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.top <= 0:
            self.rect.to