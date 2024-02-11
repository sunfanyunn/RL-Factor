prompt_code = """
import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
EMPTY = 0
HAZARD = 1
REVEALED = 2
NUM_HAZARDS = 10

class Game:
    def __init__(self, rows = ROWS, cols = COLS, nhazards = NUM_HAZARDS):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    def init_assets(self):
        \"\"\"
        Initialize game state variables:
        - Create the game board with hazards and numbers.
        - Keep track of uncovered cells and game over status.
        - Initialize the game with the first click.
        \"\"\"
        self.board = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.revealed = [[False for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.place_hazards()
        self.game_over = False
        self.player_won = False
        self.reset_button = ...

    def check_win(self):
        \"\"\"
        Check if the player has won.
        \"\"\"
       
    def reveal_cell(self, row, col):
        \"\"\"
        Code to uncover a cell.
        \"\"\"
        
    def surrounding_count(self, row, col):
        \"\"\"
        Code to count the number of hazards surrounding a cell.
        \"\"\"
    

    def run(self):
        \"\"\"
        Main game loop.
        \"\"\"
        self.init_assets()

        

if __name__ == "__main__":
    game = Game()
    game.run()

"""

context_prompt_code = """
import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
EMPTY = 0
BOMB = 1
REVEALED = 2
FLAGGED = 3
NUM_BOMBS = 10
class Minesweeper:
    def __init__(self, rows = ROWS, cols = COLS, nbombs = NUM_BOMBS):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")

    def init_assets(self):
        \"\"\"
        Initialize game state variables:
        - Create the game board with mines and numbers.
        - Keep track of uncovered cells and game over status.
        - Initialize the game 
        \"\"\"
        self.board = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.revealed = [[False for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.place_bombs()
        self.game_over = False
        self.player_won = False
        self.reset_button = ...
 
    def check_win(self):
        \"\"\"
        Check if the player has won.
        \"\"\"
       
    def reveal_cell(self, row, col):
        \"\"\"
        Code to uncover a cell.
        \"\"\"
        
    def surrounding_count(self, row, col):
        \"\"\"
        Code to count the number of mines surrounding a cell.
        \"\"\"

    def run(self):
        \"\"\"
        Main game loop.
        \"\"\"
        self.init_assets()

        

if __name__ == "__main__":
    game = Minesweeper()
    game.run()

"""
prompt = f"""A new game is to be developed using Python. 

High-level Game Description:
This is a single-player puzzle game played on a grid-based board.
The objective of the game is to uncover all the cells on the board that do not contain hazards while avoiding detonating any of the hazards.
Players can uncover a cell by clicking on it, revealing a number that indicates how many hazards are adjacent to that cell.
The game is won when all non-hazard cells are uncovered, and it is lost if a hazard is uncovered.

The game should adhere to the following specifications:

1. The game board should consist of a grid of cells, each initially covered.
2. Some cells will contain hazards, while others will be empty.
3. Players can click on a cell to uncover it.
4. A numerical value is displayed in uncovered cells, indicating the number of hazards adjacent to that cell.
5. The number of hazards remaining to be found should be displayed on the screen.
6. The game should display a message when the player wins or loses.
7. The player should have the option to start a new game after a win or loss.
8. Players start the game by clicking on an initial cell, which is guaranteed not to contain a hazard.
9. The game should automatically generate hazards and calculate the numbers for adjacent cells after the first click.
10. When a player clicks on a cell with no adjacent hazards, the game should recursively uncover adjacent empty cells until it encounters cells with numbers or the board's edge.
11. If a player clicks on a cell containing a hazard, the game should end, and the player loses.
12. The game is won when all non-hazard cells are uncovered.

Follow the structure provided below and complete the game implementation:
```python
{prompt_code}
```
"""
context_prompt = f"""A new game is to be developed using Python.

High-level Game Description:
This is a single-player puzzle game played on a grid-based board.
The objective of the game is to uncover all the cells on the board that do not contain mines while avoiding detonating any of the mines.
Players can uncover a cell by clicking on it, revealing a number that indicates how many mines are adjacent to that cell.
The game is won when all non-mine cells are uncovered, and it is lost if a mine is uncovered.

The game should adhere to the following specifications:

1. The game board should consist of a grid of cells, each initially covered.
2. Some cells will contain mines, while others will be empty.
3. Players can click on a cell to uncover it.
4. A numerical value is displayed in uncovered cells, indicating the number of mines adjacent to that cell.
5. The number of mines remaining to be found should be displayed on the screen.
6. The game should display a message when the player wins or loses.
7. The player should have the option to start a new game after a win or loss.
8. Players start the game by clicking on an initial cell, which is guaranteed not to contain a mine.
9. The game should automatically generate mines and calculate the numbers for adjacent cells after the first click.
10. When a player clicks on a cell with no adjacent mines, the game should recursively uncover adjacent empty cells until it encounters cells with numbers or the board's edge.
11. If a player clicks on a cell containing a mine, the game should end, and the player loses.
12. The game is won when all non-mine cells are uncovered.
13. The game should detect when the player has won or lost and display an appropriate message.

Follow the structure provided below and complete the game implementation:
```python
{context_prompt_code}
```
"""

complete_backbone_code = """
import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
RESTART_OFFSET = 50

CELL_SIZE = 30
ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = SCREEN_WIDTH // CELL_SIZE
NUM_BOMBS = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (70, 130, 180)

EMPTY = 0
BOMB = 1
REVEALED = 2
FLAGGED = 3


class Game:
    def __init__(self, rows=ROWS, cols=COLS, nbombs=NUM_BOMBS):
        \"\"\"
        Initialize the Minesweeper game.
        \"\"\"
        self.rows = rows
        self.cols = cols
        self.nbombs = nbombs
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.cols * CELL_SIZE, self.rows * CELL_SIZE + RESTART_OFFSET)
        )
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.init_assets()

    def init_assets(self):
        \"\"\"
        Initialize game assets, including the game board, bombs, and restart button.
        \"\"\"
        pass

    def place_bombs(self):
        \"\"\"
        Randomly place bombs on the game board.
        \"\"\"
        pass

    def reveal_cell(self, row, col):
        \"\"\"
        Reveal a cell on the game board.
        \"\"\"
        pass

    def surrounding_count(self, row, col):
        \"\"\"
        Count the number of bombs in the surrounding cells.
        \"\"\"
        pass

    def check_win(self):
        \"\"\"
        Check if the player has won the game.
        \"\"\"
        pass

    def render_background(self):
        \"\"\"
        Render the background grid on the screen.
        \"\"\"
        pass

    def render_assets(self):
        \"\"\"
        Render the revealed cells, bombs, and game over screen.
        \"\"\"
        pass

    def draw_grid(self):
        \"\"\"
        Draw the grid lines on the game board.
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

complete_code_prompt = f"""A new game is to be developed using Python.

High-level Game Description:
This is a single-player puzzle game played on a grid-based board.
The objective of the game is to uncover all the cells on the board that do not contain mines while avoiding detonating any of the mines.
Players can uncover a cell by clicking on it, revealing a number that indicates how many mines are adjacent to that cell.
The game is won when all non-mine cells are uncovered, and it is lost if a mine is uncovered.

The game should adhere to the following specifications:

1. The game board should consist of a grid of cells, each initially covered.
2. Some cells will contain mines, while others will be empty.
3. Players can click on a cell to uncover it.
4. A numerical value is displayed in uncovered cells, indicating the number of mines adjacent to that cell.
5. The number of mines remaining to be found should be displayed on the screen.
6. The game should display a message when the player wins or loses.
7. The player should have the option to start a new game after a win or loss.
8. Players start the game by clicking on an initial cell, which is guaranteed not to contain a mine.
9. The game should automatically generate mines and calculate the numbers for adjacent cells after the first click.
10. When a player clicks on a cell with no adjacent mines, the game should recursively uncover adjacent empty cells until it encounters cells with numbers or the board's edge.
11. If a player clicks on a cell containing a mine, the game should end, and the player loses.
12. The game is won when all non-mine cells are uncovered.
13. The game should detect when the player has won or lost and display an appropriate message.

Follow the structure provided below and complete the game implementation:
```python
{complete_backbone_code}
```
"""
