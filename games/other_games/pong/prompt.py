prompt_code = """
import pygame
import sys

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PAUSE_GAME = 1000
BALL_RADIUS = 15
BALL_SPEED = [3, 3]
PADDLE_SPEED = 5
PADDLE_DIMS = [10, 60]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_DIMS = [140, 40]
BUTTON_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (100, 100, 100)
# Define more constants if needed

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, up_key, down_key):
        super().__init__()
        \"\"\"
        Initialize the x, y and keys for the paddle
        \"\"\"

    def update(self):
        \"\"\"
        This will be called every game loop
        \"\"\"



class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        \"\"\"
        Initialize the x, y position on screen
        \"\"\"
        
    def update(self):
        \"\"\"
        This will be called every game loop
        \"\"\"

    def reset_ball(self):
        \"\"\"
        Reset the ball position and speed
        \"\"\"
        
class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.all_sprites = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()
        self.ball = pygame.sprite.GroupSingle()
        self.init_assets()
    
    def init_assets(self):
        # Initialize game state variables here, e.g., paddle sprites, ball_sprite, scores etc.
        self.ball_sprite = Ball()
        self.left_paddle_sprite = ...
        self.right_paddle_sprite = ...
        self.left_score=0
        self.right_score=0
        self.reset_button = ...
        pass
    
    def reset_game(self, event):
        \"\"\"
        Reset the game
        \"\"\"
        pass
    
    def run(self):
        # Main game loop
        
        

if __name__ == "__main__":
    game = Game()
    game.run()

"""
prompt = f"""Design a new game using Pygame. 

High-level Game Description:
This is a two player game.
Players control paddles on either side of the screen and use them to hit a ball back and forth.
The objective is to prevent the ball from passing your paddle while trying to get it past your opponent's paddle.

The game should adhere to the following specifications:

1. The game screen should have a black background.
2. There should be two paddles, one on the left and one on the right, initially positioned in the middle of their respective sides.
3. A ball should be in the center of the screen at the start of the game.
4. The score of Player 1 should be displayed on the left side of the screen.
5. The score of Player 2 should be displayed on the right side of the screen.
6. Players control their paddles using keyboard input.
   - Player 1 uses the "W" and "S" keys to move their paddle up and down.
   - Player 2 uses the "Up" and "Down" arrow keys to move their paddle up and down.
7. The ball should bounce off the paddles and the top and bottom edges of the screen.
8. If a player fails to hit the ball and it passes their paddle, the opposing player scores a point.
9. The game should go on endlessly until one of the players presses reset.
10. After each point scored or when the game starts, the ball should be reset to the center and move in a random direction.


Follow the structure provided as follows and complete the game implementation:
```python
{prompt_code}
```

"""


context_prompt_code = """
import pygame
import sys

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PAUSE_GAME = 1000
BALL_RADIUS = 15
BALL_SPEED = [3, 3]
PADDLE_SPEED = 5
PADDLE_DIMS = [10, 60]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_DIMS = [140, 40]
BUTTON_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (100, 100, 100)
# Define more constants if needed

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, up_key, down_key):
        super().__init__()
        \"\"\"
        Initialize the x, y and keys for the paddle
        \"\"\"

    def update(self):
        \"\"\"
        This will be called every game loop
        \"\"\"



class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        \"\"\"
        Initialize the x, y position on screen
        \"\"\"
        
    def update(self):
        \"\"\"
        This will be called every game loop
        \"\"\"

    def reset_ball(self):
        \"\"\"
        Reset the ball position and speed
        \"\"\"
        
class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.all_sprites = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()
        self.ball = pygame.sprite.GroupSingle()
        self.init_assets()
    
    def init_assets(self):
        # Initialize game state variables here, e.g., paddle sprites, ball_sprite, scores etc.
        self.ball_sprite = Ball()
        self.left_paddle_sprite = ...
        self.right_paddle_sprite = ...
        self.left_score=0
        self.right_score=0
        self.reset_button = ...
        pass
    
    def reset_game(self, event):
        \"\"\"
        Reset the game
        \"\"\"
        pass
    
    def run(self):
        # Main game loop
        
        

if __name__ == "__main__":
    game = PongGame()
    game.run()

"""
context_prompt = f"""
Design a new game using Pygame. 

High-level Game Description:
This is a two player game.
Players control paddles on either side of the screen and use them to hit a ball back and forth.
The objective is to prevent the ball from passing your paddle while trying to get it past your opponent's paddle.

The game should adhere to the following specifications:

1. The game screen should have a black background.
2. There should be two paddles, one on the left and one on the right, initially positioned in the middle of their respective sides.
3. A ball should be in the center of the screen at the start of the game.
4. The score of Player 1 should be displayed on the left side of the screen.
5. The score of Player 2 should be displayed on the right side of the screen.
6. Players control their paddles using keyboard input.
   - Player 1 uses the "W" and "S" keys to move their paddle up and down.
   - Player 2 uses the "Up" and "Down" arrow keys to move their paddle up and down.
7. The ball should bounce off the paddles and the top and bottom edges of the screen.
8. If a player fails to hit the ball and it passes their paddle, the opposing player scores a point.
9. The game should go on endlessly until one of the players presses reset.
10. After each point scored or when the game starts, the ball should be reset to the center and move in a random direction.

Follow the structure provided as follows and complete the game implementation:
```python
{context_prompt_code}
```
"""

complete_backbone_code = """
import pygame
import sys
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PAUSE_GAME = 1000
BALL_RADIUS = 15
BALL_SPEED = [3, 3]
PADDLE_SPEED = 5
PADDLE_DIMS = [10, 60]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_DIMS = [140, 40]
BUTTON_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (100, 100, 100)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, up_key, down_key):
        \"\"\"
        Initialize a Paddle object.
        \"\"\"
        super().__init__()
        self.image = pygame.Surface(PADDLE_DIMS)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        \"\"\"
        Update the paddle's position based on user input.
        \"\"\"
        keys = pygame.key.get_pressed()
        

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        \"\"\"
        Initialize a Ball object.
        \"\"\"
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self):
        \"\"\"
        Update the ball's position and check for collisions.
        \"\"\"
        self.rect.move_ip(*BALL_SPEED)

    def reset_ball(self):
        \"\"\"
        Reset the ball's position.
        \"\"\"


class Game:
    def __init__(self):
        \"\"\"
        Initialize the Game class, setting up the game window and assets.
        \"\"\"
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.font = pygame.font.Font(None, 36)
        self.all_sprites = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()
        self.ball = pygame.sprite.GroupSingle()
        self.init_assets()

    def init_assets(self):
        \"\"\"
        Initialize game assets, including paddles, ball, and reset button.
        \"\"\"
        pass

    def reset_game(self, event):
        \"\"\"
        Reset the game when the reset button is clicked.
        \"\"\"
        pass

    def render_game(self):
        \"\"\"
        Render the game elements on the screen.
        \"\"\"
        pass

    def run(self):
        \"\"\"
        Main game loop. Handle events, update the game state, and render the game.
        \"\"\"
        pass


if __name__ == "__main__":
    game = Game()
    game.run()

"""

complete_code_prompt = f"""
Design a new game using Pygame. 

High-level Game Description:
This is a two player game.
Players control paddles on either side of the screen and use them to hit a ball back and forth.
The objective is to prevent the ball from passing your paddle while trying to get it past your opponent's paddle.

The game should adhere to the following specifications:

1. The game screen should have a black background.
2. There should be two paddles, one on the left and one on the right, initially positioned in the middle of their respective sides.
3. A ball should be in the center of the screen at the start of the game.
4. The score of Player 1 should be displayed on the left side of the screen.
5. The score of Player 2 should be displayed on the right side of the screen.
6. Players control their paddles using keyboard input.
   - Player 1 uses the "W" and "S" keys to move their paddle up and down.
   - Player 2 uses the "Up" and "Down" arrow keys to move their paddle up and down.
7. The ball should bounce off the paddles and the top and bottom edges of the screen.
8. If a player fails to hit the ball and it passes their paddle, the opposing player scores a point.
9. The game should go on endlessly until one of the players presses reset.
10. After each point scored or when the game starts, the ball should be reset to the center and move in a random direction.

Follow the structure provided as follows and complete the game implementation:
```python
{complete_backbone_code}
```
"""


iterative_prompt = """feature two paddles on the screen, one on the left and one on the right.
the paddles should be able to move vertically, controlled by the players.
There should be a ball that moves horizontally between the paddles.
The player's score should be displayed at the top-center of the screen.
The game should have a simple background or borders to define the play area.
The ball should bounce off the top and bottom borders of the screen and the paddles.
When the ball passes a paddle and reaches the left or right border, the opposing player scores a point.
The game should end when a player reaches a predefined score (e.g., 5 points).
After a player wins, display "Player X Wins!" where X is the winning player, and offer the option to restart.
The player can choose to start a new game after a win.
"""
