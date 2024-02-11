# iterative_prompts = """Feature a copter character as a rectangular object on the screen.
# Generate red obstacles every half a second and move them from right to left. Each obstacle should have a random gap for the copter to pass through.
# Implement gravity to make the copter fall.
# Allow the player to make the copter jump by clicking the mouse.
# Display the player's score at the top-left corner of the screen.
# End the game when the copter collides with the ground or obstacles.
# Score based on the number of obstacles successfully passed without collision.
# Show "Game Over!" on collision and provide an option to restart.
# Allow the player to start a new game after a collision.
# Create an endless game, continuously generating obstacles as the player progresses.
# """

iterative_prompts = """
Design a helicopter character represented by a simple square shape. The helicopter should be able to move vertically within the game window using the up and down arrow keys.
Implement a gravity system, causing the helicopter to descend continuously unless the player provides input to counteract it. The player can control the ascent of the helicopter by holding the up arrow key.
Allow the helicopter to move horizontally only when the player presses the left or right arrow keys. The horizontal movement should be limited to avoid collisions with the game window boundaries.
Introduce obstacles in the form of randomly generated pixel art structures or moving objects. These obstacles should vary in height, requiring the player to navigate the helicopter through gaps and openings.
Implement collision detection so that the game ends if the helicopter collides with the obstacles or the top/bottom of the game window. When the game ends, display a "Game Over!" message and stop all in-game motion.
Incorporate a scoring system, where the player earns points for successfully navigating through gaps between obstacles. Display the current score prominently on the screen during gameplay.
Ensure the game has no predefined end and that new obstacles continue to appear, maintaining consistent difficulty as the game progresses.
Provide an option for the player to restart the game after it ends, allowing them to play again. Display a "Restart" option on the game over screen for this purpose.
"""
