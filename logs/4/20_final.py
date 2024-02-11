
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
        
        # The acceleration due to gravity affecting the bird
        self.gravity = float(0.2)
        
        # The current vertical velocity of the bird considering gravity
        self.bird_vertical_velocity = float(0.0)
        
        # The value by which the bird's vertical velocity increases when the player inputs a flap
        self.flap_power = float(-5.0)
        
        # The terminal velocity of the bird (the maximum speed at which the bird can fall)
        self.terminal_velocity = float(10.0)
        
        # The x-coordinate for the rightmost position to start drawing pipes
        self.pipe_spawn_x = int(800)
        
        # Vertical space between the upper and lower pipes
        self.pipe_gap = int(150)
        
        # The color of the pipes in RGB format, which should not be white
        self.pipe_color = tuple(tuple((0, 255, 0)))
        
        # Width of each pipe
        self.pipe_width = int(50)
        
        # Height of the upper part of a pipe pair, with a default that ensures a gap
        self.pipe_upper_height = int(200)
        
        # Velocity at which the pipes move left across the screen
        self.pipe_velocity = int(5)
        
        # The time interval in frames between spawning new pipe pairs
        self.pipe_spawn_interval = int(90)
        
        # Counter to track the frames elapsed since the last pipe spawn
        self.frame_counter = int(0)
        
        # List of positions of pipe pairs, where each pair is a dictionary with x, upper_y, and lower_y
        self.pipes_list = list([{'x': 800, 'upper_y': 0, 'lower_y': 350}])
        
def handle_bird_movement(state_manager, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            state_manager.bird_y_position -= state_manager.bird_velocity
        elif event.key == pygame.K_DOWN:
            state_manager.bird_y_position += state_manager.bird_velocity

def handle_bird_flap(state_manager, event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        state_manager.bird_vertical_velocity += state_manager.flap_power

def handle_bird_jump(state_manager, event):
    if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP)):
        state_manager.bird_vertical_velocity = state_manager.flap_power


def update_bird_position(state_manager):
    bird_bottom = state_manager.bird_y_position + state_manager.bird_height
    bird_top = state_manager.bird_y_position
    if bird_bottom > state_manager.SCREEN_HEIGHT:
        state_manager.bird_y_position = state_manager.SCREEN_HEIGHT - state_manager.bird_height
    elif bird_top < 0:
        state_manager.bird_y_position = 0

def apply_gravity_and_update_position(state_manager):
    state_manager.bird_vertical_velocity += state_manager.gravity
    if state_manager.bird_vertical_velocity > state_manager.terminal_velocity:
        state_manager.bird_vertical_velocity = state_manager.terminal_velocity
    state_manager.bird_y_position += state_manager.bird_vertical_velocity
    if state_manager.bird_y_position < 0:
        state_manager.bird_y_position = 0
    if state_manager.bird_y_position + state_manager.bird_height > state_manager.SCREEN_HEIGHT:
        state_manager.bird_y_position = state_manager.SCREEN_HEIGHT - state_manager.bird_height


def spawn_and_move_pipes(state_manager):
    state_manager.frame_counter += 1
    # Move existing pipes
    for pipe in state_manager.pipes_list:
        pipe['x'] -= state_manager.pipe_velocity
    # Remove off-screen pipes
    state_manager.pipes_list = [pipe for pipe in state_manager.pipes_list if pipe['x'] > -state_manager.pipe_width]
    # Spawn new pipes
    if state_manager.frame_counter >= state_manager.pipe_spawn_interval:
        new_pipe_height = random.randint(50, state_manager.SCREEN_HEIGHT - state_manager.pipe_gap - 50)
        state_manager.pipes_list.append({'x': state_manager.pipe_spawn_x, 'upper_y': new_pipe_height - state_manager.pipe_upper_height, 'lower_y': new_pipe_height + state_manager.pipe_gap})
        state_manager.frame_counter = 0

def check_for_collisions(state_manager):
    bird_rect = pygame.Rect(state_manager.bird_x_position, state_manager.bird_y_position, state_manager.bird_width, state_manager.bird_height)
    for pipe in state_manager.pipes_list:
        upper_rect = pygame.Rect(pipe['x'], pipe['upper_y'], state_manager.pipe_width, state_manager.pipe_upper_height)
        lower_rect = pygame.Rect(pipe['x'], pipe['lower_y'], state_manager.pipe_width, state_manager.SCREEN_HEIGHT - pipe['lower_y'])
        if bird_rect.colliderect(upper_rect) or bird_rect.colliderect(lower_rect):
            state_manager.game_over = True
            return
    if state_manager.bird_y_position + state_manager.bird_height >= state_manager.SCREEN_HEIGHT:
        state_manager.game_over = True

def render_bird(state_manager):
    # Clear the previous frame (handled in main game loop)
    # Draw the bird as a rectangle
    bird_rect = pygame.Rect(state_manager.bird_x_position, state_manager.bird_y_position, state_manager.bird_width, state_manager.bird_height)
    pygame.draw.rect(state_manager.screen, state_manager.bird_color, bird_rect)

def render_pipes(state_manager):
    for pipe in state_manager.pipes_list:
        # Draw the upper pipe
        pygame.draw.rect(state_manager.screen, state_manager.pipe_color, pygame.Rect(pipe['x'], 0, state_manager.pipe_width, pipe['upper_y']))
        # Calculate the starting y-coordinate of the lower pipe by adding upper pipe height and the gap
        lower_pipe_y = pipe['upper_y'] + state_manager.pipe_gap
        # Draw the lower pipe
        pygame.draw.rect(state_manager.screen, state_manager.pipe_color, pygame.Rect(pipe['x'], lower_pipe_y, state_manager.pipe_width, state_manager.SCREEN_HEIGHT - lower_pipe_y))

def render_game_over_screen(state_manager):
    if state_manager.game_over:
        # Define the font for the message
        font = pygame.font.SysFont(None, 55)
        # Create the text surface
        text_surface = font.render('Game Over', True, (255, 0, 0))
        # Get the width and height of the text surface
        text_width, text_height = text_surface.get_size()
        # Calculate the center position for the text surface
        x = (state_manager.SCREEN_WIDTH - text_width) // 2
        y = (state_manager.SCREEN_HEIGHT - text_height) // 2
        # Render the text surface on the screen
        state_manager.screen.blit(text_surface, (x, y))
        pygame.display.flip()


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

        # Modify the bird's vertical velocity by a certain amount upwards when the user inputs a flap (up arrow key), counteracting gravity. When the up arrow is pressed, increase bird's vertical velocity by the flap power value.
        handle_bird_flap(state_manager, event)

        # Detect a mouse click or spacebar key press and trigger a 'jump' action for the bird which temporarily overcomes gravity. This should be treated as a flap action, similar to pressing the up arrow key. The 'jump' action should then be reflected in the bird's vertical velocity.
        handle_bird_jump(state_manager, event)


        # call all the logics
        # This function should ensure that the bird's vertical movement does not go beyond the boundaries of the gameplay screen. If the bird's position is such that moving further up or down would exceed the screen height, the bird's position should be adjusted to stay within the screen limits.
        update_bird_position(state_manager)

        # Apply gravity to the bird's vertical velocity within each game tick, ensuring it doesn't exceed terminal velocity, and update the bird's y-position accordingly. Prevent the bird from moving beyond the gameplay screen's boundaries.
        apply_gravity_and_update_position(state_manager)

        # Periodically generates and updates positions of new pipe pairs with random heights, ensuring there is a gap between the pipes for the bird to pass through. Pipes should move from the right to the left of the screen, and new pipes should be generated after a specified interval.
        spawn_and_move_pipes(state_manager)

        # This function checks if there is any collision between the bird and the pipes or the bottom of the game window. For each pipe in the state manager's pipes_list, it assesses whether the bird's rectangle intersects with either the upper or lower pipe. It also checks if the bird has collided with the bottom of the game window. If a collision is detected, the game should end by setting a state variable that indicates the game is over.
        check_for_collisions(state_manager)


        # Fill the screen with white
        state_manager.screen.fill((255, 255, 255))  
        # This function should render the bird on the game screen as a rectangle using the current state variables of the bird's position, width, height, and color. It should also clear the previous frame before drawing the new one.
        render_bird(state_manager)

        # Renders the pipes on the screen with the updated positions and heights as specified in the state. Each pipe pair should be drawn at its x-coordinate, with appropriate heights for the upper and lower pipes.
        render_pipes(state_manager)

        # This function is responsible for displaying a game over message or screen when the game ends. It should be triggered by a state variable that indicates the game is over, and it should prevent any further game updates or input handling once activated.
        render_game_over_screen(state_manager)


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
