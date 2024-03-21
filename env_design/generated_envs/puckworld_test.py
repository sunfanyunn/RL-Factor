import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
import sys
import random
import numpy as np
import math


class State:
    def __init__(self, name, value, variable_type, description):
        self.name = name
        self.value = value
        self.variable_type = variable_type
        self.description = description

class StateManager:
    def __init__(self):
        # height of the gameplay screen
        self.SCREEN_HEIGHT = int(1000)
        
        # width of the gameplay screen
        self.SCREEN_WIDTH = int(1000)
        
        # fps of the gameplay screen
        self.FPS = int(60)
        
        # the score of the (human) player
        self.score = int(0)
        
        # a boolean variable indicating whether the game has ended or not
        self.game_over = bool(False)
        
        # the x and y position of the agent
        self.agent_position = {"x": 100, "y": 250}
        
        # the x and y position of the green dot
        self.green_dot_position = {"x": 400, "y": 300}
        
        # the x and y position of the red puck
        self.red_puck_position = {"x": 700, "y": 300}
        
        # Radius of the agent character represented as a blue circle
        self.agent_radius = int(20)
        
        # Color of the agent character, not white as background is white
        self.agent_color = tuple(tuple((0, 0, 255)))
        
        # The velocity of the agent character in pixels per frame
        self.agent_velocity = int(5)
        
        # The velocity of the green dot in pixels per frame on the x-axis
        self.green_dot_velocity_x = int(3)
        
        # The velocity of the green dot in pixels per frame on the y-axis
        self.green_dot_velocity_y = int(3)
        
        # Radius of the green dot
        self.green_dot_radius = int(10)
        
        # Color of the green dot, not white as background is white
        self.green_dot_color = tuple(tuple((0, 255, 0)))
        
        # The x and y position of the red puck that follows the agent
        self.red_puck_position = {'x': 700, 'y': 300}
        
        # The velocity of the red puck in pixels per frame on the x-axis as it follows the agent
        self.red_puck_velocity_x = int(1)
        
        # The velocity of the red puck in pixels per frame on the y-axis as it follows the agent
        self.red_puck_velocity_y = int(1)
        
        # Radius of the red puck
        self.red_puck_radius = int(30)
        
        # Color of the red puck, not white as background is white
        self.red_puck_color = tuple(tuple((255, 0, 0)))
        
        # The state indicating the direction of the agent's movement on the x-axis, controlled by the player
        self.agent_direction_x = int(0)
        
        # The state indicating the direction of the agent's movement on the y-axis, controlled by the player
        self.agent_direction_y = int(0)
        
        # The weight of the reward based on the agent's closeness to the green dot
        self.green_dot_closeness_reward_weight = float(1.0)
        
        # The weight of the penalty based on the agent's closeness to the red puck
        self.red_puck_closeness_penalty_weight = float(1.5)
        
        # Font size of the score display
        self.score_font_size = int(30)
        
        # Font color of the score display, not white as background is white
        self.score_font_color = tuple(tuple((0, 0, 0)))
        
        # Top-left corner position for score display to start
        self.score_position = tuple(tuple((10, 10)))
        
        # A boolean to stop spawning new obstacles/enemies, making the gameplay endless
        self.endless_mode = bool(True)
        
def update_direction_based_on_input(state_manager, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            state_manager.agent_position['y'] -= state_manager.agent_velocity
        elif event.key == pygame.K_DOWN:
            state_manager.agent_position['y'] += state_manager.agent_velocity
        elif event.key == pygame.K_LEFT:
            state_manager.agent_position['x'] -= state_manager.agent_velocity
        elif event.key == pygame.K_RIGHT:
            state_manager.agent_position['x'] += state_manager.agent_velocity

def HandleArrowKeyPress(state_manager, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            state_manager.agent_direction_x = -1
        elif event.key == pygame.K_RIGHT:
            state_manager.agent_direction_x = 1
        elif event.key == pygame.K_UP:
            state_manager.agent_direction_y = -1
        elif event.key == pygame.K_DOWN:
            state_manager.agent_direction_y = 1
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and state_manager.agent_direction_x == -1:
            state_manager.agent_direction_x = 0
        elif event.key == pygame.K_RIGHT and state_manager.agent_direction_x == 1:
            state_manager.agent_direction_x = 0
        elif event.key == pygame.K_UP and state_manager.agent_direction_y == -1:
            state_manager.agent_direction_y = 0
        elif event.key == pygame.K_DOWN and state_manager.agent_direction_y == 1:
            state_manager.agent_direction_y = 0


def move_agent(state_manager):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        state_manager.agent_position['x'] = max(0, state_manager.agent_position['x'] - state_manager.agent_velocity)
    if keys[pygame.K_RIGHT]:
        state_manager.agent_position['x'] = min(state_manager.SCREEN_WIDTH, state_manager.agent_position['x'] + state_manager.agent_velocity)
    if keys[pygame.K_UP]:
        state_manager.agent_position['y'] = max(0, state_manager.agent_position['y'] - state_manager.agent_velocity)
    if keys[pygame.K_DOWN]:
        state_manager.agent_position['y'] = min(state_manager.SCREEN_HEIGHT, state_manager.agent_position['y'] + state_manager.agent_velocity)


def move_green_dot(state_manager):
    # Update the position of the green dot
    state_manager.green_dot_position['x'] += state_manager.green_dot_velocity_x
    state_manager.green_dot_position['y'] += state_manager.green_dot_velocity_y
    # Check for collision with boundaries
    if (state_manager.green_dot_position['x'] < 0 + state_manager.green_dot_radius) or (state_manager.green_dot_position['x'] > state_manager.SCREEN_WIDTH - state_manager.green_dot_radius):
        # Reflect the green dot's velocity and assign a new random velocity for x-axis
        state_manager.green_dot_velocity_x = random.randint(1, 5) * (-1 if state_manager.green_dot_velocity_x > 0 else 1)
        state_manager.green_dot_position['x'] += state_manager.green_dot_velocity_x
    if (state_manager.green_dot_position['y'] < 0 + state_manager.green_dot_radius) or (state_manager.green_dot_position['y'] > state_manager.SCREEN_HEIGHT - state_manager.green_dot_radius):
        # Reflect the green dot's velocity and assign a new random velocity for y-axis
        state_manager.green_dot_velocity_y = random.randint(1, 5) * (-1 if state_manager.green_dot_velocity_y > 0 else 1)
        state_manager.green_dot_position['y'] += state_manager.green_dot_velocity_y

def move_red_puck(state_manager):
    direction_x = 1 if state_manager.agent_position['x'] > state_manager.red_puck_position['x'] else -1
    direction_y = 1 if state_manager.agent_position['y'] > state_manager.red_puck_position['y'] else -1
    state_manager.red_puck_position['x'] += state_manager.red_puck_velocity_x * direction_x
    state_manager.red_puck_position['y'] += state_manager.red_puck_velocity_y * direction_y
    state_manager.red_puck_position['x'] = max(state_manager.red_puck_radius, min(state_manager.red_puck_position['x'], state_manager.SCREEN_WIDTH - state_manager.red_puck_radius))
    state_manager.red_puck_position['y'] = max(state_manager.red_puck_radius, min(state_manager.red_puck_position['y'], state_manager.SCREEN_HEIGHT - state_manager.red_puck_radius))

def UpdateAgentPosition(state_manager):
    # Calculate new position
    new_x = state_manager.agent_position['x'] + (state_manager.agent_velocity * state_manager.agent_direction_x)
    new_y = state_manager.agent_position['y'] + (state_manager.agent_velocity * state_manager.agent_direction_y)
    
    # Ensure the agent stays within the screen boundaries
    new_x = max(0, min(new_x, state_manager.SCREEN_WIDTH))
    new_y = max(0, min(new_y, state_manager.SCREEN_HEIGHT))
    
    # Update the agent position
    state_manager.agent_position['x'] = new_x
    state_manager.agent_position['y'] = new_y

def update_score_based_on_proximity(state_manager):
    def distance(pos1, pos2):
        return ((pos1['x'] - pos2['x']) ** 2 + (pos1['y'] - pos2['y']) ** 2) ** 0.5

    if not state_manager.game_over:
        distance_to_green_dot = distance(state_manager.agent_position, state_manager.green_dot_position)
        closeness_to_green_dot = max(0, state_manager.SCREEN_HEIGHT - distance_to_green_dot)
        distance_to_red_puck = distance(state_manager.agent_position, state_manager.red_puck_position)
        closeness_to_red_puck = max(0, state_manager.SCREEN_HEIGHT - distance_to_red_puck)
        state_manager.score += (state_manager.green_dot_closeness_reward_weight * closeness_to_green_dot - state_manager.red_puck_closeness_penalty_weight * closeness_to_red_puck) / state_manager.FPS
        state_manager.score = round(state_manager.score, 2)  # Keep the score to two decimal places

def EnableEndlessMode(state_manager):
    state_manager.endless_mode = True

def reposition_green_dot_if_reached(state_manager):
    # Calculate the distance between agent and green dot
    distance = ((state_manager.agent_position['x'] - state_manager.green_dot_position['x']) ** 2 + (state_manager.agent_position['y'] - state_manager.green_dot_position['y']) ** 2) ** 0.5
    # Check if agent has reached the green dot
    if distance <= state_manager.green_dot_radius:
        valid_position = False
        while not valid_position:
            # Generate a random new position for green dot
            new_x = random.randint(0, state_manager.SCREEN_WIDTH)
            new_y = random.randint(0, state_manager.SCREEN_HEIGHT)
            # Ensure the new position does not overlap with the agent or the red puck
            if (abs(new_x - state_manager.agent_position['x']) > state_manager.green_dot_radius*2) and (abs(new_y - state_manager.agent_position['y']) > state_manager.green_dot_radius*2) and (abs(new_x - state_manager.red_puck_position['x']) > state_manager.green_dot_radius*2) and (abs(new_y - state_manager.red_puck_position['y']) > state_manager.green_dot_radius*2):
                valid_position = True
        # Update the green dot's position
        state_manager.green_dot_position['x'] = new_x
        state_manager.green_dot_position['y'] = new_y


def draw_agent(state_manager):
    pygame.draw.circle(state_manager.screen, state_manager.agent_color, (state_manager.agent_position['x'], state_manager.agent_position['y']), state_manager.agent_radius)

def draw_green_dot(state_manager):
    pygame.draw.circle(state_manager.screen, state_manager.green_dot_color, (state_manager.green_dot_position['x'], state_manager.green_dot_position['y']), state_manager.green_dot_radius)

def draw_red_puck(state_manager):
    pygame.draw.circle(state_manager.screen, state_manager.red_puck_color, (state_manager.red_puck_position['x'], state_manager.red_puck_position['y']), state_manager.red_puck_radius)

def render_score(state_manager):
    font = pygame.font.SysFont(None, state_manager.score_font_size)
    text = font.render('Score: {}'.format(state_manager.score), True, state_manager.score_font_color)
    state_manager.screen.blit(text, state_manager.score_position)

def RenderEndlessModeIndicator(state_manager):
    if state_manager.endless_mode:
        font = pygame.font.SysFont(None, 24)
        text = font.render('Endless Mode', True, (0, 0, 0))
        state_manager.screen.blit(text, (state_manager.SCREEN_WIDTH - 150, 10))


class Game():
    def __init__(self):
        self.state_manager = StateManager()
        self.state_manager.screen = pygame.display.set_mode((self.state_manager.SCREEN_WIDTH,
                                                             self.state_manager.SCREEN_HEIGHT))

    def run(self, event):
        state_manager = self.state_manager
        if event.type == pygame.QUIT:
            return False
        # This function should listen for arrow key presses (up, down, left, right) and update the direction variable accordingly, indicating the direction in which the agent should move. No movement is applied in this function, only the intended direction of motion is recorded.
        update_direction_based_on_input(state_manager, event)

        # This function should capture the arrow key presses and update the agent_direction_x and agent_direction_y state variables in the StateManager instance to reflect the movement direction indicated by the keypresses. If the left arrow key is pressed, agent_direction_x should be -1; if right, agent_direction_x should be 1; if up, agent_direction_y should be -1; if down, agent_direction_y should be 1. Releasing the keys should reset the corresponding direction variable to 0.
        HandleArrowKeyPress(state_manager, event)


        # call all the logics
        # Based on the direction set by the input handling function, this function computes the new position of the agent by changing the agent_position 'x' and 'y' values. The agent's velocity defined in self.agent_velocity is used to determine how much the position changes. This function also ensures that the agent remains within the boundaries of the screen.
        move_agent(state_manager)

        # This function should calculate the new position of the green dot based on its current velocity while ensuring the dot remains within the boundaries of the screen. If the dot hits a boundary, its velocity should change to a new random value, causing it to move in a different random direction.
        move_green_dot(state_manager)

        # This function should calculate the new position of the red puck. The puck should follow the agent's last known position, moving closer each frame by reducing the distance between the puck's current position and the agent's position. The movement speed is dictated by the red puck's defined velocities in the x and y axes. Additionally, it should ensure that the red puck does not exit the screen boundaries and adjust its position accordingly.
        move_red_puck(state_manager)

        # This function should modify the position of the agent by applying the direction indicated by the agent_direction_x and agent_direction_y state variables. Multiply the agent_velocity by the direction variables to find the change in position, and update the agent_position 'x' and 'y' values accordingly. Make sure that the agent stays within the boundaries of the screen.
        UpdateAgentPosition(state_manager)

        # Update the player's score each frame based on the distance between the agent and the green dot and between the agent and the red puck. The score increases when the agent is closer to the green dot and decreases when too close to the red puck, considering the respective weights for closeness reward and closeness penalty.
        update_score_based_on_proximity(state_manager)

        # To support endless gameplay, this function should modify the state manager's endless_mode variable to true, ensuring that the game logic does not have a terminal state and new obstacles can be generated indefinitely.
        EnableEndlessMode(state_manager)

        # Check if the agent has reached the green dot and, if so, randomly reposition the green dot to a new location within the boundaries of the screen using the provided `green_dot_new_position_x` and `green_dot_new_position_y` as the coordinates for the new position. The new coordinates should be random but ensure they are within the screen's boundaries and not overlapping the agent or red puck.
        reposition_green_dot_if_reached(state_manager)


        # Fill the screen with white
        state_manager.screen.fill((255, 255, 255))  
        # This function takes the current state of the agent, including position and other properties, to render the agent on the screen. It draws a blue circle at the agent's position with a radius specified by self.agent_radius using the self.agent_color.
        draw_agent(state_manager)

        # This function should render the green dot on the screen at its current `green_dot_position`, using its `green_dot_color` and `green_dot_radius` state variables.
        draw_green_dot(state_manager)

        # This function should draw the red puck onto the screen at its updated position secured from the state variables. It should use the red puck's color, radius, and position state variables to draw a red circle representing the red puck.
        draw_red_puck(state_manager)

        # Render the updated score in the top-left corner of the screen using the state_manager's `score` state variable. The displayed score should be in a readable font with the size and color specified by the state_manager's `score_font_size` and `score_font_color`. The score should be rendered at the `score_position`, allowing the player to keep track of their score in real time while playing the game.
        render_score(state_manager)

        # This function should continuously update the UI to reflect the active endless gameplay status by possibly adding an indicator on the UI showing that endless mode is active.
        RenderEndlessModeIndicator(state_manager)


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
