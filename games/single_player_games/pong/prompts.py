iterative_prompts = """Create a paddle character for the human player, represented as a rectangle, positioned on one side of the screen. 
Allow the human player to control the paddle's vertical movement using the up and down arrow keys.
Implement a paddle character for the CPU opponent, also represented as a rectangle, positioned on the opposite side of the screen.
Enable the CPU to control its paddle's vertical movement to autonomously track the ball.
Introduce a ball that moves horizontally across the screen. The ball should bounce off the paddles and the top and bottom walls of the game window.
Detect collisions between the ball and the paddles. When the ball collides with a paddle, make it bounce off in the opposite direction.
Introduce scoring mechanics, where the human player earns a point if the CPU fails to return the ball, and vice versa. 
Display the current score at the top of the screen.
Ensure the game has no predefined end, allowing for continuous play. 
Display a "Game Over!" message when one player reaches a predefined score limit.
Provide an option for the player to restart the game after the "Game Over" screen is displayed."""
