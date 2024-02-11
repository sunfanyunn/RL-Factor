context_prompt_code = """
import pygame
import sys
import time
import random
from pygame.locals import *

WHITE = (255, 255, 255)
GREEN = (77, 204, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Game_2048:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(
            (450, 600)
        )  
        pygame.display.set_caption("2048")

        self.myfont = pygame.font.SysFont(None, 50)
        self.score =0
        self.board = self.init_board()
        self.reset_button = pygame.Rect(
            175, 550, 100, 40
        )  # Define the reset button rectangle

    def init_board(self):
        \"\"\"
        Init game
        \"\"\"
        self.board = []

    def add_new_num(self, n):
        \"\"\"
        Add new number to the board
        \"\"\"

    def check_win(self):
        \"\"\"
        Check if the player has won
        \"\"\"

    def can_move(self):
        \"\"\"
        Check if the player can move
        \"\"\"

    def check_lose(self):
        \"\"\"
        Check if the player has lost
        \"\"\"

    def main(self, UserInput):
        \"\"\"
        This function should update the game board based on the user input.
        \"\"\"

    def update_score(self, move):
         
         \"\"\"
        Update the score when tiles are merged
        \"\"\"
     
        
    def reset(self):
       \"\"\"
        Reset the game board and score
        \"\"\"

    def run(self):
        \"\"\"
        please implement the main game loop here
        \"\"\"


if __name__ == "__main__":
    game = Game_2048()
    game.run()
    

"""

context_prompt = f"""Implement the following game using Pygame:

High-level Game Description:
Players will take control of a grid filled with numbered tiles and aim to reach the 2048 tile.

The game should adhere to the following gameplay specifications:
1. The game screen should feature a grid of numbered tiles.
2. The current score should be displayed prominently on the screen, updating as players merge tiles.
3. A reset button should be readily accessible for players at the bottom of the screen.
4. Tiles in the game should start with two random values of either 2 or 4, placed in random positions on the grid.
5. Players can manipulate the tiles' positions using arrow keys (Up, Down, Left, Right).
6. When a move is made, all tiles on the grid should slide in the chosen direction until they hit the wall or another tile.
7. If two tiles with the same number collide during a move, they should merge into one tile with a value equal to their sum. This merging can only happen once per move.
8. The objective is to continuously combine tiles, increasing their values, and ultimately reaching the 2048 tile.
9. The game should end when the player reaches the 2048 tile and wins, or when there are no more valid moves left, signifying a loss.
10. The game should go on endlessly until one of the players presses the reset button to start a new game.
Follow the structure provided as follows and complete the game implementation:
```python
{context_prompt_code}
```
"""


prompt_code = """
import pygame
import sys
import time
import random
from pygame.locals import *

WHITE = (255, 255, 255)
GREEN = (77, 204, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(
            (450, 600)
        )  
    

        self.myfont = pygame.font.SysFont(None, 50)
        self.score =0
        self.board = self.init_board()
        self.reset_button = pygame.Rect(
            175, 550, 100, 40
        )  # Define the reset button rectangle

    def init_board(self):
        \"\"\"
        Init game
        \"\"\"
        self.board = []

    def add_new_num(self, n):
        \"\"\"
        Add new number to the board
        \"\"\"

    def check_win(self):
        \"\"\"
        Check if the player has won
        \"\"\"

    def can_move(self):
        \"\"\"
        Check if the player can move
        \"\"\"

    def check_lose(self):
        \"\"\"
        Check if the player has lost
        \"\"\"

    def main(self, UserInput):
        \"\"\"
        This function should update the game board based on the user input.
        \"\"\"

    def update_score(self, move):
         
         \"\"\"
        Update the score when tiles are merged
        \"\"\"
     
        
    def reset(self):
       \"\"\"
        Reset the game board and score
        \"\"\"

    def run(self):
        \"\"\"
        please implement the main game loop here
        \"\"\"


if __name__ == "__main__":
    game = Game()
    game.run()

"""
prompt = f"""
Implement the following game using Pygame, where the game will be played in multiples of 3:

High-level Game Description:
Players will take control of a grid filled with numbered tiles and aim to reach the 768 tile.

The game should adhere to the following gameplay specifications, with the change that the objective is to continuously combine tiles in multiples of 3, increasing their values, and ultimately reaching the 612 tile:

1. The game screen should feature a grid of numbered tiles.
2. The current score should be displayed prominently on the screen, updating as players merge tiles in multiples of 3.
3. A reset button should be readily accessible for players at the bottom of the screen.
4. Tiles in the game should start with two random values of either 3 or 6, placed in random positions on the grid.
5. Players can manipulate the tiles' positions using arrow keys (Up, Down, Left, Right).
6. When a move is made, all tiles on the grid should slide in the chosen direction until they hit the wall or another tile.
7. If two tiles with the same number collide during a move, they should merge into one tile with a value equal to their sum. This merging can only happen once per move.
8. The objective is to continuously combine tiles in multiples of 3, increasing their values, and ultimately reaching the 768 tile.
9. The game should end when the player reaches the 768 tile and wins or when there are no more valid moves left, signifying a loss.
10. The game should go on endlessly until one of the players presses the reset button to start a new game.

Follow the structure provided as follows and complete the game implementation:
```python
{prompt_code}
```
"""
complete_backbone_code = """
import pygame
import sys
import time
import random
from pygame.locals import *

WHITE = (255, 255, 255)
GREEN = (77, 204, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Game:
    def __init__(self):
        \"\"\"
        Initialize the 2048 game.
        \"\"\"
        pygame.init()
        self.window = pygame.display.set_mode(
            (450, 600)
        )  
        pygame.display.set_caption("2048")

        self.myfont = pygame.font.SysFont(None, 50)
        self.score =0
        self.board = self.init_board()
        self.reset_button = pygame.Rect(
            175, 550, 100, 40
        )  # Define the reset button rectangle

    def init_board(self):
        \"\"\"
        Initialize the game board.
        \"\"\"
        self.board = []

    def add_new_num(self, n):
        \"\"\"
        Add new numbers to the board.
        \"\"\"
        pass

    def check_win(self):
        \"\"\"
        Check if the player has won.
        \"\"\"
        pass

    def add(self, i_list, j_list, i_direction, j_direction):
        \"\"\"
        Perform addition of tiles in a specified direction.
        \"\"\"
        pass

    def push(self, i_list, j_list, i_direction, j_direction):
        \"\"\"
        Push tiles in a specified direction.
        \"\"\"
        pass

    def push_direction(self, UserInput):
        \"\"\"
        Perform pushing tiles in the specified direction based on user input.
        \"\"\"
        pass

    def check_cell(self, i, j):
        \"\"\"
        Check if a cell has a matching neighbor.
        \"\"\"
        pass

    def can_move(self):
        \"\"\"
        Check if there are valid moves left on the board.
        \"\"\"
        pass

    def check_lose(self):
        \"\"\"
        Check if the player has lost the game.
        \"\"\"
        pass

    def main(self, UserInput):
        \"\"\"
        Main function to handle user input and update the game state.
        \"\"\"
        pass

    def update_score(self, move):
        \"\"\"
        Update the score based on the number of moves.
        \"\"\"
        pass

    def reset(self):
        \"\"\"
        Reset the game board and score.
        \"\"\"
        pass

    def build_text(self, i, j):
        \"\"\"
        Build text for displaying numbers on the board.
        \"\"\"
        pass

    def show_text(self):
        \"\"\"
        Display the numbers on the game board.
        \"\"\"
        pass

    def quit_window(self, event):
        \"\"\"
        Quit the game window.
        \"\"\"
        pass

    def game_over(self):
        \"\"\"
        Display "Game Over" message.
        \"\"\"
        pass

    def win(self):
        \"\"\"
        Display "You WIN" message.
        \"\"\"
        pass

    def run(self):
        \"\"\"
        Main game loop.
        \"\"\"
        blocks = []
        for i in range(4):
            for j in range(4):
                blocks.append(
                    [pygame.Rect((i * 100) + 30, (j * 100) + 135, 90, 90), WHITE]
                )

        while True:
            for event in pygame.event.get():
                pass

if __name__ == "__main__":
    game = Game()
    game.run()
"""

complete_code_prompt = f"""Implement the following game using Pygame:

High-level Game Description:
Players will take control of a grid filled with numbered tiles and aim to reach the 2048 tile.

The game should adhere to the following gameplay specifications:
1. The game screen should feature a grid of numbered tiles.
2. The current score should be displayed prominently on the screen, updating as players merge tiles.
3. A reset button should be readily accessible for players at the bottom of the screen.
4. Tiles in the game should start with two random values of either 2 or 4, placed in random positions on the grid.
5. Players can manipulate the tiles' positions using arrow keys (Up, Down, Left, Right).
6. When a move is made, all tiles on the grid should slide in the chosen direction until they hit the wall or another tile.
7. If two tiles with the same number collide during a move, they should merge into one tile with a value equal to their sum. This merging can only happen once per move.
8. The objective is to continuously combine tiles, increasing their values, and ultimately reaching the 2048 tile.
9. The game should end when the player reaches the 2048 tile and wins, or when there are no more valid moves left, signifying a loss.
10. The game should go on endlessly until one of the players presses the reset button to start a new game.
Follow the structure provided as follows and complete the game implementation:
```python
{complete_backbone_code}
```
"""
