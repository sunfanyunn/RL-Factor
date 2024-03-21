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
        
        # x and y position of the ball, and the speed in the x and y directions
        self.ball = {"x": 200, "y": 200, "speed_x": 5, "speed_y": 5}
        
        # the x and y position of the player's paddle
        self.player_paddle = {"x": 100, "y": 100}
        
        # the x and y position of the player's paddle
        self.cpu_paddle = {"x": 900, "y": 100}
        
        # the score of the cpu player
        self.cpu_score = int(0)
        
        # Width of the player's paddle
        self.player_paddle_width = int(15)
        
        # Height of the player's paddle
        self.player_paddle_height = int(100)
        
        # Color of the player's paddle
        self.player_paddle_color = tuple(tuple((0, 128, 255)))
        
        # Speed of the player's paddle movement
        self.player_paddle_speed = int(10)
        
        # Current state of the UP arrow key (pressed or not)
        self.up_key_pressed = bool(False)
        
        # Current state of the DOWN arrow key (pressed or not)
        self.down_key_pressed = bool(False)
        
        # Width of the CPU paddle which will be the same as the player's paddle to maintain consistency
        self.cpu_paddle_width = int(15)
        
        # Height of the CPU's paddle which will be the same as the player's paddle to maintain consistency
        self.cpu_paddle_height = int(100)
        
        # Color of the CPU's paddle which should not be white
        self.cpu_paddle_color = tuple(tuple((255, 0, 0)))
        
        # Speed of the CPU's paddle movement
        self.cpu_paddle_speed = int(10)
        
        # Color of the ball which should not be white as the background is white
        self.ball_color = tuple(tuple((255, 255, 0)))
        
        # Radius of the ball
        self.ball_radius = int(10)
        
        # Indicates whether a collision occurred with the player's paddle
        self.collision_with_player_paddle = bool(False)
        
        # Indicates whether a collision occurred with the CPU's paddle
        self.collision_with_cpu_paddle = bool(False)
        
        # Points to be awarded to the player or CPU when the opposing side fails to return the ball
        self.points_per_missed_return = int(1)
        
        # Font size for displaying the score
        self.score_font_size = int(30)
        
        # Font color for displaying the score
        self.score_font_color = tuple(tuple((0, 0, 0)))
        
        # Top margin to offset the score display from the top edge of the screen
        self.score_top_margin = int(10)
        
        # Message displayed when the game is over
        self.game_over_message = str("""Game Over!""")
        
        # X position for the 'Game Over!' message
        self.game_over_message_x = int(500)
        
        # Y position for the 'Game Over!' message
        self.game_over_message_y = int(500)
        
        # Message displayed with the option to restart the game
        self.restart_game_message = str("""Press R to Restart""")
        
        # X position for the restart game message
        self.restart_game_message_x = int(500)
        
        # Y position for the restart game message
        self.restart_game_message_y = int(550)
        
def handle_player_input(state_manager, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            state_manager.player_paddle['y'] = max(0, state_manager.player_paddle['y'] - state_manager.player_paddle_speed)
        elif event.key == pygame.K_DOWN:
            state_manager.player_paddle['y'] = min(state_manager.SCREEN_HEIGHT - state_manager.player_paddle_height, state_manager.player_paddle['y'] + state_manager.player_paddle_speed)

def handle_paddle_movement_input(state_manager, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            state_manager.up_key_pressed = True
        elif event.key == pygame.K_DOWN:
            state_manager.down_key_pressed = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            state_manager.up_key_pressed = False
        elif event.key == pygame.K_DOWN:
            state_manager.down_key_pressed = False

def handle_restart_game_input(state_manager, event):
    if state_manager.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        state_manager.score = 0
        state_manager.cpu_score = 0
        state_manager.player_paddle = {'x': 100, 'y': 100}
        state_manager.cpu_paddle = {'x': 900, 'y': 100}
        state_manager.ball = {'x': 200, 'y': 200, 'speed_x': 5, 'speed_y': 5}
        state_manager.game_over = False

def update_player_paddle_position(state_manager):
    if state_manager.up_key_pressed and state_manager.player_paddle['y'] > 0:
        state_manager.player_paddle['y'] -= state_manager.player_paddle_speed
    if state_manager.down_key_pressed and state_manager.player_paddle['y'] < state_manager.SCREEN_HEIGHT - state_manager.player_paddle_height:
        state_manager.player_paddle['y'] += state_manager.player_paddle_speed


def update_cpu_paddle_position(state_manager):
    # Determine the middle y-position of the CPU paddle
    cpu_paddle_middle = state_manager.cpu_paddle['y'] + state_manager.cpu_paddle_height / 2

    # Move CPU paddle towards the ball's y-position
    if state_manager.ball['y'] > cpu_paddle_middle and (state_manager.cpu_paddle['y'] + state_manager.cpu_paddle_height < state_manager.SCREEN_HEIGHT):
        state_manager.cpu_paddle['y'] += state_manager.cpu_paddle_speed
    elif state_manager.ball['y'] < cpu_paddle_middle and state_manager.cpu_paddle['y'] > 0:
        state_manager.cpu_paddle['y'] -= state_manager.cpu_paddle_speed

    # Ensure the CPU paddle stays within the screen bounds
    if state_manager.cpu_paddle['y'] < 0:
        state_manager.cpu_paddle['y'] = 0
    elif state_manager.cpu_paddle['y'] + state_manager.cpu_paddle_height > state_manager.SCREEN_HEIGHT:
        state_manager.cpu_paddle['y'] = state_manager.SCREEN_HEIGHT - state_manager.cpu_paddle_height


def update_ball_position(state_manager):
    # Update ball position based on its current speed
    state_manager.ball['x'] += state_manager.ball['speed_x']
    state_manager.ball['y'] += state_manager.ball['speed_y']

    # Check for collision with top and bottom walls
    if state_manager.ball['y'] <= 0 or state_manager.ball['y'] >= state_manager.SCREEN_HEIGHT:
        state_manager.ball['speed_y'] *= -1

    # Check for collision with player paddle
    if (state_manager.ball['x'] <= state_manager.player_paddle['x'] + state_manager.player_paddle_width and
            state_manager.player_paddle['y'] < state_manager.ball['y'] < state_manager.player_paddle['y'] + state_manager.player_paddle_height):
        state_manager.ball['speed_x'] *= -1

    # Check for collision with CPU paddle
    if (state_manager.ball['x'] >= state_manager.cpu_paddle['x'] - state_manager.cpu_paddle_width and
            state_manager.cpu_paddle['y'] < state_manager.ball['y'] < state_manager.cpu_paddle['y'] + state_manager.cpu_paddle_height):
        state_manager.ball['speed_x'] *= -1

    # Check for scoring
    if state_manager.ball['x'] <= 0:  # CPU scores
        state_manager.cpu_score += 1
        state_manager.ball['x'], state_manager.ball['y'] = state_manager.SCREEN_WIDTH // 2, state_manager.SCREEN_HEIGHT // 2
        state_manager.ball['speed_x'] = 5  # Give the ball a default speed in X direction
        state_manager.ball['speed_y'] = 5  # Give the ball a default speed in Y direction
    elif state_manager.ball['x'] >= state_manager.SCREEN_WIDTH:  # Player scores
        state_manager.score += 1
        state_manager.ball['x'], state_manager.ball['y'] = state_manager.SCREEN_WIDTH // 2, state_manager.SCREEN_HEIGHT // 2
        state_manager.ball['speed_x'] = -5 # Give the ball a default speed in X direction
        state_manager.ball['speed_y'] = 5  # Give the ball a default speed in Y direction

def update_ball_collision(state_manager):
    # Check for collision with player paddle
    if (state_manager.ball['x'] - state_manager.ball_radius <= state_manager.player_paddle['x'] + state_manager.player_paddle_width and
        state_manager.ball['x'] + state_manager.ball_radius >= state_manager.player_paddle['x'] and
        state_manager.ball['y'] - state_manager.ball_radius <= state_manager.player_paddle['y'] + state_manager.player_paddle_height and
        state_manager.ball['y'] + state_manager.ball_radius >= state_manager.player_paddle['y']):
        state_manager.ball['speed_x'] *= -1
        state_manager.collision_with_player_paddle = True
    else:
        state_manager.collision_with_player_paddle = False

    # Check for collision with CPU paddle
    if (state_manager.ball['x'] + state_manager.ball_radius >= state_manager.cpu_paddle['x'] - state_manager.cpu_paddle_width and
        state_manager.ball['x'] - state_manager.ball_radius <= state_manager.cpu_paddle['x'] and
        state_manager.ball['y'] + state_manager.ball_radius >= state_manager.cpu_paddle['y'] and
        state_manager.ball['y'] - state_manager.ball_radius <= state_manager.cpu_paddle['y'] + state_manager.cpu_paddle_height):
        state_manager.ball['speed_x'] *= -1
        state_manager.collision_with_cpu_paddle = True
    else:
        state_manager.collision_with_cpu_paddle = False


def update_scores_and_reset_ball(state_manager):
    if state_manager.ball['x'] < 0:
        state_manager.cpu_score += state_manager.points_per_missed_return
        state_manager.ball = {'x': state_manager.SCREEN_WIDTH // 2, 'y': state_manager.SCREEN_HEIGHT // 2, 'speed_x': 5, 'speed_y': 5}
    elif state_manager.ball['x'] > state_manager.SCREEN_WIDTH:
        state_manager.score += state_manager.points_per_missed_return
        state_manager.ball = {'x': state_manager.SCREEN_WIDTH // 2, 'y': state_manager.SCREEN_HEIGHT // 2, 'speed_x': -5, 'speed_y': 5}


def remove_game_ending_conditions(state_manager):
    # Since we want to remove the conditions that end the game,
    # the simplest way is to make sure 'game_over' is always False.
    state_manager.game_over = False

def check_for_game_over_condition(state_manager):
    if state_manager.score >= 5 or state_manager.cpu_score >= 5:
        state_manager.game_over = True

def render_player_paddle(state_manager):
    pygame.draw.rect(state_manager.screen, state_manager.player_paddle_color, pygame.Rect(state_manager.player_paddle['x'], state_manager.player_paddle['y'], state_manager.player_paddle_width, state_manager.player_paddle_height))

def render_cpu_paddle(state_manager):
    pygame.draw.rect(state_manager.screen, state_manager.cpu_paddle_color, pygame.Rect(state_manager.cpu_paddle['x'], state_manager.cpu_paddle['y'], state_manager.cpu_paddle_width, state_manager.cpu_paddle_height))

def render_ball(state_manager):
    pygame.draw.circle(state_manager.screen, state_manager.ball_color, (state_manager.ball['x'], state_manager.ball['y']), state_manager.ball_radius)

def render_scores(state_manager):
    font = pygame.font.Font(None, state_manager.score_font_size)
    player_score_text = font.render(str(state_manager.score), True, state_manager.score_font_color)
    cpu_score_text = font.render(str(state_manager.cpu_score), True, state_manager.score_font_color)

    # Calculate the positions for the score
    mid_screen = state_manager.SCREEN_WIDTH // 2
    player_score_position = (mid_screen - 50 - player_score_text.get_width(), state_manager.score_top_margin)
    cpu_score_position = (mid_screen + 50, state_manager.score_top_margin)

    # Display the scores
    state_manager.screen.blit(player_score_text, player_score_position)
    state_manager.screen.blit(cpu_score_text, cpu_score_position)

def remove_end_game_ui_elements(state_manager):
    if state_manager.game_over:
        # Don't render anything that would suggest the game is over
        pass
    else:
        # Continue rendering the game as usual
        render_player_paddle(state_manager)
        render_cpu_paddle(state_manager)
        render_ball(state_manager)
        render_scores(state_manager)

def render_game_over_screen(state_manager):
    if state_manager.game_over:
        font = pygame.font.Font(None, state_manager.score_font_size)
        game_over_text = font.render(state_manager.game_over_message, True, state_manager.score_font_color)
        restart_text = font.render(state_manager.restart_game_message, True, state_manager.score_font_color)

        # Calculate the positions for the text
        game_over_position = (state_manager.game_over_message_x - game_over_text.get_width()//2, state_manager.game_over_message_y)
        restart_position = (state_manager.restart_game_message_x - restart_text.get_width()//2, state_manager.restart_game_message_y)

        # Display the messages
        state_manager.screen.blit(game_over_text, game_over_position)
        state_manager.screen.blit(restart_text, restart_position)


class Game():
    def __init__(self):
        self.state_manager = StateManager()
        self.state_manager.screen = pygame.display.set_mode((self.state_manager.SCREEN_WIDTH,
                                                             self.state_manager.SCREEN_HEIGHT))

    def run(self, event):
        state_manager = self.state_manager
        if event.type == pygame.QUIT:
            return False
        # Detects when the player presses the up or down arrow key and signals that the player's paddle should move up or down respectively.
        handle_player_input(state_manager, event)

        # Detects when the player presses and releases the up or down arrow key and updates state variables to indicate whether the paddle should be moving up, stopped, or moving down.
        handle_paddle_movement_input(state_manager, event)

        # This function should detect when the 'R' key is pressed after the game over screen is displayed. It should reset the scores, the paddle positions, the ball properties, and the 'game_over' flag to restart the game.
        handle_restart_game_input(state_manager, event)


        # call all the logics
        # Based on the current input state variables, update the player's paddle position ensuring it stays within the screen boundaries.
        update_player_paddle_position(state_manager)

        # Autonomously move the CPU paddle vertically in response to the ball's y position so as to keep the paddle aligned with the ball, ensuring that the CPU paddle does not move beyond the boundaries of the screen.
        update_cpu_paddle_position(state_manager)

        # This function should move the ball horizontally, checking for collisions with the paddles as well as with the top and bottom edges of the game window. If the ball collides with a paddle, it should reverse its horizontal direction. If it collides with the top or bottom walls, it should reverse its vertical direction. It should also handle scoring by checking if the ball passes beyond the left or right edges of the screen, indicating a point for the CPU or player respectively, and then repositioning the ball to the center for the next round.
        update_ball_position(state_manager)

        # The function should check if the ball's x and y coordinates overlap with the paddles’ x and y coordinates respectively. If a collision with either paddle is detected, the function must reverse the horizontal direction of the ball, updating the 'speed_x' value to its negative. The function should also update the 'collision_with_player_paddle' or 'collision_with_cpu_paddle' to True if a collision occurs with the respective paddle.
        update_ball_collision(state_manager)

        # Detect when the ball goes past the player's or the CPU's paddle and update the respective scores. Then reset the ball's position and speed to start a new round.
        update_scores_and_reset_ball(state_manager)

        # Remove any conditions or checks that would set the game's 'game_over' state variable to True. This will allow the game state to continue without reaching an end based on predefined conditions such as time limits, score limits, or other game-ending events.
        remove_game_ending_conditions(state_manager)

        # This function should check if either player's or the CPU's score has reached 5. If so, it should transition the state of the game to 'game_over'. This function will be used to determine when to display the 'Game Over!' message and offer the option to restart.
        check_for_game_over_condition(state_manager)


        # Fill the screen with white
        state_manager.screen.fill((255, 255, 255))  
        # Draws the player's paddle as a rectangle at the player's paddle's current x and y positions using the dimensions and color specified in the state variables.
        render_player_paddle(state_manager)

        # Draw the CPU's paddle as a rectangle at the CPU's paddle's current x and y positions using the dimensions and color specified in the state variables.
        render_cpu_paddle(state_manager)

        # This function will draw the ball on the screen as a circle using the ball's current state variables for its position, radius, and color.
        render_ball(state_manager)

        # Render the player's and CPU's current scores at the top of the game screen, in a specified font size, font color, and with an offset from the top edge based on the screen width, font size, and top margin defined in the state manager. The scores should reflect the current 'score' and 'cpu_score' state variables.
        render_scores(state_manager)

        # Modify or remove any elements or screens that indicate or bring the game to a close. This includes any 'Game Over' screens, final score displays, or instruction prompts that might pause or end the game session.
        remove_end_game_ui_elements(state_manager)

        # This function should render the 'Game Over!' message and the 'Press R to Restart' instruction onto the screen when the game over condition is met, which is one of the players reaching a score of 5.
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
