prompt_code = """
import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
OFFSET = 100


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + OFFSET))
    
    def init_assets(self): 
        \"\"\"
       this function initializes the game state variables 
       :param board: the game board
       :type board: a 2D array
       :param current_player: whose turn is it, "X" or "Y"
       :type current_player: str
       :param game_over: whether the game is over or not
       :type game_over: bool
        \"\"\"
        self.board = [['' for x in range(3)] for y in range(3)]
        self.current_player = "X"
        self.game_over = False
        # Add more components if you deem necessary

    def handle_click(self, pos):
        \"\"\" 
        handles mouse click events
        :param pos: the position of the mouse click
        :type pos: tuple
        \"\"\"
        pass

    def check_win(self):
        \"\"\"
        checks if there is a winner
        :return: the winner, if there is one
        :rtype: str
        \"\"\"
        pass

    def reset_game(self):
        \"\"\" 
        resets the game
        \"\"\"
        pass
        
    def run(self):
        \"\"\" 
        main game loop
        \"\"\"
        self.init_assets()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


if __name__ == "__main__":
    game = Game()
    game.run()
"""


prompt = f"""A new game is to be designed using Pygame. 
High-level Game Description:
The game is a two-player board game played on a 3x3 grid.
Players take turns to place their symbols on the grid.
The objective is to form a line of three of their symbols either horizontally, vertically, or diagonally.

The game should adhere to the following specifications:

1. The game board should consist of a 3x3 grid where players can make their moves.
2. Player 1's symbol is represented as "X," and Player 2's symbol is represented as "O."
3. The score of Player 1 should be displayed on the left side of the screen.
4. The score of Player 2 should be displayed on the right side of the screen.
5. Players take turns to make a move by clicking on an empty cell on the grid.
6. The game should detect when a player has won by forming a line of three symbols.
7. If all cells on the board are filled without a winner, the game should declare a draw.
8. Whenever a player wins a round, their respective score should be incremented by 1.
9. The board should be reset for a new round after a winner is determined.
10. The game should allow players to start a new round after a win or draw.

Follow the structure provided as follows and complete the game implementation. You are not limited to the code provided and can add more components if you deem necessary.
```python
{prompt_code}
```
"""


context_prompt_code = """
import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
OFFSET = 100


class TicTacToeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + OFFSET))
        pygame.display.set_caption("Tic Tac Toe")
    
    def init_assets(self): 
        \"\"\"
       this function initializes the game state variables 
       :param board: the tic-tac-toe board
       :type board: a 2D array
       :param current_player: whose turn is it, "X" or "Y"
       :type current_player: str
       :param game_over: whether the game is over or not
       :type game_over: bool
        \"\"\"
        self.board = [['' for x in range(3)] for y in range(3)]
        self.current_player = "X"
        self.game_over = False
        # Add more components if you deem necessary
        
    def handle_click(self, pos):
        \"\"\" 
        handles mouse click events
        :param pos: the position of the mouse click
        :type pos: tuple
        \"\"\"
        pass
        
    def check_win(self):
        \"\"\"
        checks if there is a winner
        :return: the winner, if there is one
        :rtype: str
        \"\"\"
        pass

    def reset_game(self):
        \"\"\" 
        resets the game
        \"\"\"
        pass
        
    def run(self):
        \"\"\" 
        main game loop
        \"\"\"
        self.init_assets()


if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()
"""

context_prompt = f"""A new game is to be designed using Pygame. 
High-level Game Description:
The game is a two-player board game played on a 3x3 grid.
Players take turns to place their symbols on the grid.
The objective is to form a line of three of their symbols either horizontally, vertically, or diagonally.

The game should adhere to the following specifications:

1. The game board should consist of a 3x3 grid where players can make their moves.
2. Player 1's symbol is represented as "X," and Player 2's symbol is represented as "O."
3. The score of Player 1 should be displayed on the left side of the screen.
4. The score of Player 2 should be displayed on the right side of the screen.
5. Players take turns to make a move by clicking on an empty cell on the grid.
6. The game should detect when a player has won by forming a line of three symbols.
7. If all cells on the board are filled without a winner, the game should declare a draw.
8. Whenever a player wins a round, their respective score should be incremented by 1.
9. The board should be reset for a new round after a winner is determined.
10. The game should allow players to start a new round after a win or draw.

Follow the structure provided as follows and complete the game implementation. You are not limited to the code provided and can add more components if you deem necessary.
```python
{context_prompt_code}
```
"""

complete_backbone_code = """
import pygame
import sys
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
OFFSET = 100
CELL_SIZE = SCREEN_HEIGHT // 3
LINE_WIDTH = 10
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = CELL_SIZE // 4

WHITE = (255, 255, 255)
LINE_COLOR = (23, 85, 85)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (85, 170, 85)
BUTTON_COLOR = (70, 130, 180)


class CrossSprite(pygame.sprite.Sprite):
    def __init__(self, row, col):
        \"\"\"
        Initialize a CrossSprite object.
        \"\"\"
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE - 2 * SPACE, CELL_SIZE - 2 * SPACE), pygame.SRCALPHA)

class CircleSprite(pygame.sprite.Sprite):
    def __init__(self, row, col):
        \"\"\"
        Initialize a CircleSprite object.
        \"\"\"
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE - 2 * SPACE, CELL_SIZE - 2 * SPACE), pygame.SRCALPHA)

class Game:
    def __init__(self):
        \"\"\"
        Initialize the Game class, setting up the game window.
        \"\"\"
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + OFFSET))
        pygame.display.set_caption("Tic Tac Toe")
        self.cross_sprites = pygame.sprite.Group()
        self.circle_sprites = pygame.sprite.Group()
        
    def render_background(self):
        \"\"\"
        Render the background based on the current state of the board.
        \"\"\"
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "X":
                    cross_sprite = CrossSprite(row, col)
                    self.cross_sprites.add(cross_sprite)
                elif self.board[row][col] == "O":
                    circle_sprite = CircleSprite(row, col)
                    self.circle_sprites.add(circle_sprite)

    def init_assets(self):
        \"\"\"
        this function initializes the game state variables 
       :param board: the tic-tac-toe board
       :type board: a 2D array
       :param current_player: whose turn is it, "X" or "Y"
       :type current_player: str
       :param game_over: whether the game is over or not
       :type game_over: bool
        \"\"\"
        self.board = [['' for x in range(3)] for y in range(3)]
        self.current_player = "X"
        self.game_over = False
        # Add more components if you deem necessary

    def check_win(self):
        \"\"\"
        Check if there is a winner on the current game board and return the winning player (if any).
        \"\"\"
        pass

    def reset_game(self):
        \"\"\"
        Reset the game to its initial state.
        \"\"\"
        

    def handle_click(self, pos):
        \"\"\"
        handles mouse click events
        :param pos: the position of the mouse click
        :type pos: tuple
        \"\"\"
        pass

    def display_winner(self):
        \"\"\"
        Display the winner or a draw message when the game is over.

        Also, display a restart button for the user to start a new game.
        \"\"\"
        pass

    def render_lines(self):
        \"\"\"
        Render the grid lines on the game board.
        \"\"\"
        pass

    def run(self):
        \"\"\"
        Main game loop. Handle events, update the game state, etc.
        \"\"\"
        self.init_assets()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

if __name__ == "__main__":
    game = Game()
    game.run()


"""

complete_code_prompt = f"""
A new game is to be designed using Pygame. 
High-level Game Description:
The game is a two-player board game played on a 3x3 grid.
Players take turns to place their symbols on the grid.
The objective is to form a line of three of their symbols either horizontally, vertically, or diagonally.

The game should adhere to the following specifications:

1. The game board should consist of a 3x3 grid where players can make their moves.
2. Player 1's symbol is represented as "X," and Player 2's symbol is represented as "O."
3. The score of Player 1 should be displayed on the left side of the screen.
4. The score of Player 2 should be displayed on the right side of the screen.
5. Players take turns to make a move by clicking on an empty cell on the grid.
6. The game should detect when a player has won by forming a line of three symbols.
7. If all cells on the board are filled without a winner, the game should declare a draw.
8. Whenever a player wins a round, their respective score should be incremented by 1.
9. The board should be reset for a new round after a winner is determined.
10. The game should allow players to start a new round after a win or draw.

Follow the structure provided as follows and complete the game implementation. You are not limited to the code provided and can add more components if you deem necessary.
```python
{complete_backbone_code}
```
"""


game_specifications = [
    "Create a 3x3 grid for the game board.",
    'Assign "X" for Player 1 and "O" for Player 2.',
    "Display Player 1's score on the left and Player 2's on the right.",
    "Allow players to click on an empty cell for their turn.",
    "Detect lines of three symbols for a win.",
    "Declare a draw if all cells are filled without a winner.",
    "Increment the winning player's score by 1.",
    "Reset the game board after a win or draw.",
    "Allow players to start a new round after a win or draw.",
]


iterative_initial_prompt = """A new game is to be designed using Pygame. 
High-level Game Description:
The game is a two-player board game played on a 3x3 grid.
Players take turns to place their symbols on the grid.
The objective is to form a line of three of their symbols either horizontally, vertically, or diagonally.
"""


def get_specification_prompt(i):
    prompt = f"""
    {iterative_initial_prompt}
    Implement the following functionality:
    {game_specifications[i]}
    
    Follow the structure provided as follows:
    ```python
    {complete_backbone_code}
    ```
    """


iterative_prompts = """
Create a grid-based Tic-Tac-Toe game with a 3x3 board.
Represent the game board using a simple 3x3 array or grid, where each cell can be empty, marked by 'X,' or marked by 'O.'
Allow two players to take turns, each represented by 'X' or 'O.' The players can use the keyboard or mouse to select the cell where they want to place their mark.
Implement a check for a winning condition after each move, where a player wins if they have three of their marks in a row horizontally, vertically, or diagonally.
Detect a tie or draw situation when the board is filled, and no player has achieved a winning condition.
End the game when a player wins or when the game is a draw. Display a "Game Over!" message and provide an option for the players to restart the game.
Include a scoring system to keep track of each player's wins.
Show the current score for each player on the screen during gameplay.
Ensure the game allows for continuous play without a predefined end, with the ability to restart for multiple rounds.
"""
