
import pygame
import sys
import random
import numpy as np


class State:
    def __init__(self, name, value, variable_type, description):
        self.name = name
        self.value = value
        self.variable_type = variable_type
        self.description = description

class StateManager:
    def __init__(self):
        # height of the gameplay screen
        self.SCREEN_HEIGHT = int(600)
        
        # width of the gameplay screen
        self.SCREEN_WIDTH = int(800)
        
        # fps of the gameplay screen
        self.FPS = int(60)
        
        # The current y-coordinate of the bird character
        self.bird_y_position = int(300)
        
        # The fixed x-coordinate of the bird character
        self.bird_x_position = int(100)
        
        # Height of the bird character
        self.bird_height = int(25)
        
        # Width of the bird character
        self.bird_width = int(25)
        
        # The color of the bird character in RGB format
        self.bird_color = tuple(tuple((255, 204, 0)))
        
        # The velocity at which the bird moves up or down
        self.bird_velocity = int(5)
        
def handle_bird_movement(state_manager, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            state_manager.bird_y_position -= state_manager.bird_velocity
        elif event.key == pygame.K_DOWN:
            state_manager.bird_y_position += state_manager.bird_velocity

def update_bird_position(state_manager):
    bird_bottom = state_manager.bird_y_position + state_manager.bird_height
    bird_top = state_manager.bird_y_position
    if bird_bottom > state_manager.SCREEN_HEIGHT:
        state_manager.bird_y_position = state_manager.SCREEN_HEIGHT - state_manager.bird_height
    elif bird_top < 0:
        state_manager.bird_y_position = 0

def render_bird(state_manager):
    # Clear the previous frame (handled in main game loop)
    # Draw the bird as a rectangle
    bird_rect = pygame.Rect(state_manager.bird_x_position, state_manager.bird_y_position, state_manager.bird_width, state_manager.bird_height)
    pygame.draw.rect(state_manager.screen, state_manager.bird_color, bird_rect)


class Game():
    def __init__(self):
        self.state_manager = StateManager()
        self.state_manager.screen = pygame.display.set_mode((self.state_manager.SCREEN_WIDTH,
                                                             self.state_manager.SCREEN_HEIGHT))

    def run(self, event):
        state_manager = self.state_manager
        if event.type == pygame.QUIT:
            return False
        # This function should detect key press events for the up arrow and down arrow keys. On pressing the up arrow key, the bird should move upwards, and on pressing the down arrow key, the bird should move downwards. This function updates the bird's vertical position in state variables.
        handle_bird_movement(state_manager, event)


        # call all the logics
        # This function should ensure that the bird's vertical movement does not go beyond the boundaries of the gameplay screen. If the bird's position is such that moving further up or down would exceed the screen height, the bird's position should be adjusted to stay within the screen limits.
        update_bird_position(state_manager)


        # Fill the screen with white
        state_manager.screen.fill((255, 255, 255))  
        # This function should render the bird on the game screen as a rectangle using the current state variables of the bird's position, width, height, and color. It should also clear the previous frame before drawing the new one.
        render_bird(state_manager)


        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    global event
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
        pygame.display.flip()
    pygame.quit()
