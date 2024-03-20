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
        
        # the x position of the catcher
        self.catcher_position_x = int(100)
        
        # the y position of the catcher
        self.catcher_position_y = int(950)
        
        # the number of lives the player has
        self.lives = int(3)
        
        # a list of dictionaries representing the x and y positions of the balls
        self.balls = list([{"x": 500, "y": 100}])
        
        # Width of the catcher rectangle
        self.catcher_width = int(100)
        
        # Height of the catcher rectangle
        self.catcher_height = int(20)
        
        # Color of the catcher rectangle
        self.catcher_color = tuple(tuple((255, 0, 0)))
        
        # The speed at which the catcher moves horizontally
        self.catcher_speed_x = int(5)
        
        # The state of the left arrow key (True if pressed, False otherwise)
        self.left_key_pressed = bool(False)
        
        # The state of the right arrow key (True if pressed, False otherwise)
        self.right_key_pressed = bool(False)
        
        # Width of the ball.
        self.ball_width = int(20)
        
        # Height of the ball.
        self.ball_height = int(20)
        
        # Color of the balls, not white.
        self.ball_color = tuple(tuple((0, 255, 0)))
        
        # The spawn rate of the balls, in terms of frames.
        self.ball_spawn_rate = int(120)
        
        # A variable to keep track of frames since the last ball spawn. To be incremented each frame and reset when a new ball spawns.
        self.frames_since_last_ball = int(0)
        
        # The maximum number of balls allowed on the screen at the same time.
        self.max_balls_on_screen = int(5)
        
        # The vertical position where the balls will spawn. Typically this will be just off-screen or at the very top, such as 0 or a small negative value.
        self.ball_spawn_y = int(-20)
        
        # The vertical speed at which each ball moves downwards
        self.ball_speed_y = int(3)
        
        # The variable to hold the increase in ball speed, per level or score threshold
        self.ball_speed_increment = int(1)
        
        # The threshold score after which ball speed should increase, could be score or time
        self.ball_speed_increase_threshold = int(10)
        
        # Current ball speed increase based on the game progression
        self.current_ball_speed_increase = int(0)
        
        # Font to be used for score display
        self.score_font = str('Arial')
        
        # Font size for displaying the score
        self.score_font_size = int(30)
        
        # Color of the score text, not white
        self.score_color = tuple(tuple((0, 0, 0)))
        
        # Position of the score on the screen (x, y)
        self.score_position = tuple(tuple((10, 10)))
        
        # A flag to indicate if a life was lost in the current frame
        self.life_lost = bool(False)
        
        # Boolean flag to indicate when to display the game over message
        self.display_game_over = bool(False)
        
        # Message to display when the game is over
        self.game_over_message = str('Game Over!')
        
        # X position for displaying the game over message, horizontally centered
        self.game_over_message_x = int(500)
        
        # Y position for displaying the game over message, vertically centered
        self.game_over_message_y = int(500)
        
        # Duration in frames to display the game over message before continuing
        self.game_over_display_duration = int(180)
        
        # Frame counter to control the duration of the game over message display
        self.game_over_frame_counter = int(0)
        
        # Flag to indicate the transition to a game over state and handle the halt in gameplay
        self.game_over_initiated = bool(False)
        
        # A sound effect to play when the game ends, if desired.
        self.game_over_sound = str("""game_over.wav""")
        
        # A boolean variable indicating whether a click to restart the game has been registered
        self.restart_clicked = bool(False)
        
        # X position range of the clickable area to restart the game (it could be the whole screen or a button area)
        self.restart_clickable_x_range = tuple(tuple((0, self.SCREEN_WIDTH)))
        
        # Y position range of the clickable area to restart the game (it could be the whole screen or a button area)
        self.restart_clickable_y_range = tuple(tuple((0, self.SCREEN_HEIGHT)))
        
        # The score after which the size of the catcher would reduce
        self.catcher_size_reduction_threshold = int(20)
        
        # The amount by which the catcher's width should reduce after each threshold is met
        self.catcher_width_reduction = int(10)
        
        # Tracks the number of times catcher's size has been reduced
        self.catcher_size_reductions = int(0)
        
        # The minimum allowed width for the catcher to avoid making the game impossible
        self.minimum_catcher_width = int(20)
        
def update_key_press_states(state_manager, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            state_manager.left_key_pressed = True
        elif event.key == pygame.K_RIGHT:
            state_manager.right_key_pressed = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            state_manager.left_key_pressed = False
        elif event.key == pygame.K_RIGHT:
            state_manager.right_key_pressed = False

def handle_restart_click(state_manager, event):
    if state_manager.game_over and event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        if (state_manager.restart_clickable_x_range[0] <= mouse_x <= state_manager.restart_clickable_x_range[1]) and (state_manager.restart_clickable_y_range[0] <= mouse_y <= state_manager.restart_clickable_y_range[1]):
            state_manager.restart_clicked = True

def update_catcher_position(state_manager):
    if state_manager.left_key_pressed:
        state_manager.catcher_position_x = max(0, state_manager.catcher_position_x - state_manager.catcher_speed_x)
    if state_manager.right_key_pressed:
        state_manager.catcher_position_x = min(state_manager.SCREEN_WIDTH - state_manager.catcher_width, state_manager.catcher_position_x + state_manager.catcher_speed_x)

def spawn_random_ball(state_manager):
    state_manager.frames_since_last_ball += 1
    if state_manager.frames_since_last_ball >= state_manager.ball_spawn_rate and len(state_manager.balls) < state_manager.max_balls_on_screen:
        random_x = random.randint(0, state_manager.SCREEN_WIDTH)
        new_ball = {'x': random_x, 'y': state_manager.ball_spawn_y}
        state_manager.balls.append(new_ball)
        state_manager.frames_since_last_ball = 0


def update_ball_positions(state_manager):
    for ball in state_manager.balls:
        ball['y'] += state_manager.ball_speed_y + state_manager.current_ball_speed_increase
    if state_manager.score >= state_manager.ball_speed_increase_threshold:
        state_manager.current_ball_speed_increase += state_manager.ball_speed_increment
        state_manager.score -= state_manager.ball_speed_increase_threshold
    if state_manager.game_over:
        state_manager.current_ball_speed_increase = 0

def detect_ball_catcher_collision(state_manager):
    catcher_rect = pygame.Rect(state_manager.catcher_position_x, state_manager.catcher_position_y, state_manager.catcher_width, state_manager.catcher_height)
    for ball in state_manager.balls[:]:
        ball_rect = pygame.Rect(ball['x'], ball['y'], state_manager.ball_width, state_manager.ball_height)
        if catcher_rect.colliderect(ball_rect):
            state_manager.score += 1
            state_manager.balls.remove(ball)

def detect_missed_balls_and_reduce_lives(state_manager):
    for ball in state_manager.balls[:]:
        if ball['y'] > state_manager.catcher_position_y:
            state_manager.lives -= 1
            state_manager.balls.remove(ball)
            state_manager.life_lost = True
            if state_manager.lives <= 0:
                state_manager.game_over = True

def handle_game_over(state_manager):
    if state_manager.lives <= 0 and not state_manager.game_over_initiated:
        state_manager.game_over_initiated = True
        state_manager.game_over = True
        # Here you might want to play the game over sound (not implemented)
        # pygame.mixer.Sound(state_manager.game_over_sound).play()
    if state_manager.game_over:
        if state_manager.game_over_frame_counter < state_manager.game_over_display_duration:
            state_manager.game_over_frame_counter += 1
        else:
            # Reset the game state for a new game
            state_manager.score = 0
            state_manager.lives = 3
            state_manager.balls = [{'x': 500, 'y': 100}]
            state_manager.game_over = False
            state_manager.display_game_over = False
            state_manager.game_over_frame_counter = 0
            state_manager.game_over_initiated = False


def restart_game(state_manager):
    if state_manager.restart_clicked and state_manager.game_over:
        state_manager.score = 0
        state_manager.lives = 3
        state_manager.balls = [{'x': 500, 'y': 100}]
        state_manager.game_over = False
        state_manager.restart_clicked = False
        state_manager.current_ball_speed_increase = 0
        state_manager.frames_since_last_ball = 0
        state_manager.game_over_frame_counter = 0
        state_manager.game_over_display_duration = 180


def update_difficulty_based_on_score(state_manager):
    if state_manager.game_over:
        # Reset the difficulty enhancements
        state_manager.current_ball_speed_increase = 0
        state_manager.catcher_size_reductions = 0
    else:
        # Increase the falling speed of the ball
        score_increments = state_manager.score // state_manager.ball_speed_increase_threshold
        if score_increments > state_manager.current_ball_speed_increase:
            state_manager.current_ball_speed_increase = score_increments
            state_manager.ball_speed_y += state_manager.ball_speed_increment

        # Reduce the size of the catcher
        catcher_size_increments = state_manager.score // state_manager.catcher_size_reduction_threshold
        if catcher_size_increments > state_manager.catcher_size_reductions:
            state_manager.catcher_size_reductions = catcher_size_increments
            new_catcher_width = state_manager.SCREEN_WIDTH - state_manager.catcher_width_reduction * state_manager.catcher_size_reductions
            # Ensure catcher width does not go below the minimum allowed width
            if new_catcher_width >= state_manager.minimum_catcher_width:
                state_manager.SCREEN_WIDTH = new_catcher_width
            else:
                state_manager.SCREEN_WIDTH = state_manager.minimum_catcher_width


def draw_catcher(state_manager):
    pygame.draw.rect(state_manager.screen, state_manager.catcher_color, pygame.Rect(state_manager.catcher_position_x, state_manager.catcher_position_y, state_manager.catcher_width, state_manager.catcher_height))


def draw_balls(state_manager):
    for ball in state_manager.balls:
        pygame.draw.ellipse(state_manager.screen, state_manager.ball_color, pygame.Rect(ball['x'], ball['y'], state_manager.ball_width, state_manager.ball_height))

def display_score(state_manager):
    font = pygame.font.SysFont(state_manager.score_font, state_manager.score_font_size)
    text = font.render('Score: ' + str(state_manager.score), True, state_manager.score_color)
    state_manager.screen.blit(text, state_manager.score_position)

def display_lives(state_manager):
    font = pygame.font.SysFont('arial', 30)
    text = font.render('Lives: ' + str(state_manager.lives), True, (0, 0, 0))
    state_manager.screen.blit(text, (10, 10))

def render_game_over_message(state_manager):
    if state_manager.game_over_initiated and state_manager.game_over_frame_counter < state_manager.game_over_display_duration:
        game_over_font = pygame.font.SysFont('Arial', 50)
        game_over_text = game_over_font.render(state_manager.game_over_message, True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(state_manager.game_over_message_x, state_manager.game_over_message_y))
        state_manager.screen.blit(game_over_text, game_over_rect)


class Game():
    def __init__(self):
        self.state_manager = StateManager()
        self.state_manager.screen = pygame.display.set_mode((self.state_manager.SCREEN_WIDTH,
                                                             self.state_manager.SCREEN_HEIGHT))

    def run(self, event):
        state_manager = self.state_manager
        if event.type == pygame.QUIT:
            return False
        # This function should check if the left or right arrow keys are pressed and update the corresponding state variables 'left_key_pressed' or 'right_key_pressed' to True. If the keys are released, it should update the state variables to False.
        update_key_press_states(state_manager, event)

        # This function checks if the mouse click is within the restart_clickable_x_range and restart_clickable_y_range coordinates and if the game_over state is True. If a click is detected within these bounds while game_over is True, it should update the restart_clicked state variable to True.
        handle_restart_click(state_manager, event)


        # call all the logics
        # This function should modify the catcher's horizontal position based on the current key press states. If 'left_key_pressed' is True, the function should decrement catcher_position_x by catcher_speed_x, ensuring it does not go below zero. Similarly, if 'right_key_pressed' is True, the function should increment catcher_position_x by catcher_speed_x, ensuring it does not exceed SCREEN_WIDTH minus catcher_width.
        update_catcher_position(state_manager)

        # Periodically generate a new ball with a random x-coordinate. This function will check if frames_since_last_ball equals or exceeds ball_spawn_rate. If it does, it will create a new ball dictionary with a random x-coordinate and ball_spawn_y for the y-coordinate. It also increments frames_since_last_ball if the ball_spawn_rate is not reached and resets frames_since_last_ball to zero after spawning a ball. The function will ensure the number of balls on the screen does not exceed max_balls_on_screen and reset the counter after spawning a ball.
        spawn_random_ball(state_manager)

        # The function should update each ball's vertical position by incrementing its 'y' coordinate by the sum of ball_speed_y and current_ball_speed_increase. As the score increases, check if the score has reached the ball_speed_increase_threshold and increase current_ball_speed_increase by ball_speed_increment. Reset current_ball_speed_increase when the game resets.
        update_ball_positions(state_manager)

        # Check if any ball's rectangle intersects with the catcher's rectangle. If a collision is detected, increment the player's score by 1 and remove the ball from the balls list.
        detect_ball_catcher_collision(state_manager)

        # Detect if any ball has reached the bottom of the screen, beyond the catcher's position. If so, decrement the player's life count by one and remove the ball from the balls list. If the player's life count reaches zero, set the game_over state to True.
        detect_missed_balls_and_reduce_lives(state_manager)

        # This function checks if the player's lives have reached zero to transition to the game over state. It should trigger the display of the 'Game Over!' message and halt the gameplay without quitting the game. It should also handle the timing for how long the game over message is displayed by incrementing the game_over_frame_counter, and once the game_over_display_duration is reached, it should reset the game state for a new game.
        handle_game_over(state_manager)

        # This function should transition the state of the game from a game_over state to the initial game state when the restart_clicked boolean is True. It would reset key state variables such as score, lives, balls, game_over, and restart_clicked to their initial values.
        restart_game(state_manager)

        # Adjust the difficulty over time depending on the player's score. Increase the ball's falling speed when the player reaches certain score thresholds, and reduce the size of the catcher to make the game progressively harder. Handle resetting of difficulty enhancement variables when the game restarts to ensure that the difficulty level begins from the initial state with each new game.
        update_difficulty_based_on_score(state_manager)


        # Fill the screen with white
        state_manager.screen.fill((255, 255, 255))  
        # Draw the catcher as a rectangle at the specified catcher_position_x and catcher_position_y, with the dimensions defined in catcher_width and catcher_height, and fill it with the catcher_color.
        draw_catcher(state_manager)

        # Render the balls on the screen. Each ball is a rectangle (or other distinct shape) drawn at the coordinates specified in its dictionary inside the balls list. The balls should be rendered with the ball_color, ball_width, and ball_height attributes.
        draw_balls(state_manager)

        # Render the updated score on the top-left corner of the screen using the score_color, score_position, score_font, and score_font_size.
        display_score(state_manager)

        # Display the current number of lives the player has left on the screen, in a designated area with appropriate text and styling.
        display_lives(state_manager)

        # This function should display a 'Game Over!' message in the center of the screen when the game_over state is True. The message should be rendered using the defined game_over_message, game_over_message_x, game_over_message_y, and any styling attributes. It should only render the message if the game_over_initiated flag is set to True and game_over_frame_counter is less than game_over_display_duration.
        render_game_over_message(state_manager)


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
