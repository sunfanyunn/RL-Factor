iterative_prompts = """
Create a paddle character, represented as a rectangle, positioned at the bottom and the middle of the screen. The paddle should be movable horizontally across the bottom of the game window.
Allow the player to control the paddle's horizontal movement using the left and right arrow keys on the keyboard.
Periodically spawn a fruit with a random x-coordinate at the top of the screen. The fruit should be visually distinct and easily recognizable.
Make the fruit move downwards at a steady pace towards the paddle. The speed can be constant or increase gradually as the game progresses.
Detect collisions between the paddle and the fruit. When the paddle catches a fruit, increment the player's score and display this score in the top-left corner of the screen.
Give the player a set number of lives. Each time a fruit is missed by the paddle and reaches the bottom of the screen, decrease the player's life count by one.
End the game when the player's lives reach zero. Display a "Game Over!" message and temporarily halt gameplay.
Provide an option for the player to restart the game after the "Game Over" screen is displayed.
Continuously generate new fruits after each catch or miss, ensuring endless gameplay. Optionally, increase the game's difficulty gradually by speeding up the fruit's fall or reducing the size of the paddle as the player's score increases.
"""

context_prompt_code = """
import pygame
import sys
import random

# initialize constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


class Catcher(pygame.sprite.Sprite):
    def __init__(self, x):
        \"\"\"
        Initialize the catcher
        x should be the initial x-coordinate of the catcher
        self.rect should be a pygame.Rect object with the initial position of the catcher
        \"\"\"
        super().__init__()
        self.x = ...
        self.rect = ...

    def reset(self):
        \"\"\"
        reset the catcher to the initial position
        \"\"\"


class Ball(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        \"\"\"
        initialize the ball
        x should be the initial x-coordinate of the catcher
        self.rect should be a pygame.Rect object with the initial position of the catcher
        \"\"\"
        super().__init__()
        self.rect = ...

    def update(self):
        \"\"\"
        this will be called in the main game loop
        \"\"\"


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        \"\"\"
        Initialize / reset the game
        self.game_over is a boolean representing whether the game is over
        self.score keeps track of the player's score
        self.catch is the Catcher instance
        self.balls is a list of ball object, it should not be empty
        \"\"\"
        self.game_over = False
        self.catcher = Catcher(...)
        self.score = 0
        self.balls = []
        ...

    def run(self, event):
        \"\"\" 
        please implement the main game loop here
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