iterative_prompts = """
Create a bird character, visually represented as a simple rectangle, that remains static in the horizontal axis but can move up and down with arrow keys within the game window.
Introduce gravity, causing the bird to continuously fall unless counteracted by player input.
Allow the bird to 'jump' or move upwards in response to a player's mouse click or key press, temporarily overcoming gravity.
Periodically spawn pairs of vertical pipes moving from right to left across the screen. Each pair should have a gap for the bird to pass through, and their heights should vary randomly.
Implement collision detection so that the game ends if the bird touches the pipes or the bottom of the game window.
When the game ends, display a "Game Over!" messagea and stop all the motion of the game.
Implement a scoring system, where the player earns points each time the bird successfully passes between a pair of pipes without colliding.
Show the current score in the top-left corner of the screen during gameplay.
Ensure the game has no predefined end and that new pipes continue to generate, maintaining consistent difficulty as the game progresses.
"""

context_prompt_code = """
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PIPE_WIDTH = 80


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        \"\"\"
        self.rect is the pygame.Rect rectangle representing the bird
        \"\"\"
        super().__init__()
        self.rect = ...

    def update(self):
        \"\"\"
        This will be called every game loop
        \"\"\"


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        \"\"\"
        x stands for the the x position of this instance on screen
        rect is the pygame.Rect instance representing the pipe
        passed is a boolean representing whether the bird has passed this pipe
        \"\"\"
        super().__init__()
        self.x = x
        self.rect = ...

    def update(self):
        \"\"\"
        This will be called every game loop
        \"\"\"


class Game(pygame.sprite.Sprite):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        \"\"\"
        Initialize / reset the game
        self.game_over is a boolean representing whether the game is over
        self.bird is the Bird instance
        self.pipes is a list of Pipe instances (not a sprite.Group)
        \"\"\"
        self.game_over = False
        self.bird = Bird(...)
        self.pipes = []
        self.pipes.append(Pipe(...))
        self.all_spirtes = pygame.sprite.Group()
        ...
        
    def run(self, event):
        \"\"\" 
        please implement the game loop here, given the pygame event
        \"\"\"

if __name__ == "__main__":
    game = Game()
    pygame.init()
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()
"""