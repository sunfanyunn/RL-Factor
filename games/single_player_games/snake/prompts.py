game_specifications = [
    "Generate new food items at random screen locations after consumption or game start.",
    "Facilitate continuous snake movement in the chosen direction.",
    "Update the score display upon the snake consuming food.",
    "Increase the snake's length by one unit after consuming food.",
    "Detect collisions with walls or the snake's body, concluding the game upon detection.",
    "Respond to the reset button press by resetting the game, including score and positions.",
    "Conclude the game if the snake collides with walls or its own body.",
]

prompt = """Implement the following game using Pygame:

High-level Game Description:
Players control an eel on the screen and guide it to eat food items.
The objective is to grow the eel as long as possible without running into the walls or the eel's own body.

The game should adhere to the following gameplay specifications:
1. The game screen should have a green background.
2. The current score should be displayed on the screen.
3. The game should have a reset button at the bottom of the screen.
4. Food items are represented as small squres on the screen. After each food item is consumed or when the game starts, a new food item should appear at a random location on the screen.
5. The eel should move continuously in the direction it is facing.  
6. Players can change the direction of the eel using arrow keys (Up, Down, Left, Right).
7. The eel should grow one unit in length when it consumes a food item.
8. The game should end if the eel collides with the walls or its own body.
9. The game should go on endlessly until one of the players presses reset.

Follow the structure provided below and complete the game implementation:
"""

prompt_code = """

import pygame
import sys
import random


WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)


class Game:
    def __init__(self):
        pygame.init()
        \"\"\"
        Initialize the game screen, clock, game state, sprites and reset button
        \"\"\"
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.reset_button = pygame.Rect(20, 20, 100, 50)
        self.reset_button_active = False
        self.win_message = False
        self.all_sprites = pygame.sprite.Group()
        self.eel = Eel()
        self.food = Food()

    def reset_game(self):
        \"\"\"
        Reset the game state
        \"\"\"
        

    def update_game_state(self):
        \"\"\"
        Update the game state
        \"\"\"


    def handle_events(self):
        \"\"\"
        Handle events
        \"\"\"
    
    def run(self):
        while True:
            self.handle_events()
            self.update_game_state()
            self.render_game()


class Eel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        \"\"\"
        Initialize the eel's body,length direction and image
        \"\"\"
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        



    def change_direction(self, new_direction):
        \"\"\"
        Change the direction of the eel 
        \"\"\"
        
    def check_collision(self):
        \"\"\"
        Check whether the eel has collided with the wall or itself
        \"\"\"

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        \"\"\"
        Randomize the position of the food within the grid
        \"\"\"

if __name__ == "__main__":
    game = Game()
    game.run()

"""

context_prompt = """Implement the following game using Pygame:

High-level Game Description:
Players control a snake on the screen and guide it to eat food items.
The objective is to grow the snake as long as possible without running into the walls or the snake's own body.

The game should adhere to the following gameplay specifications:
1. The game screen should have a green background.
2. The current score should be displayed on the screen.
3. The game should have a reset button at the bottom of the screen.
4. Food items are represented as small squres on the screen. After each food item is consumed or when the game starts, a new food item should appear at a random location on the screen.
5. The snake should move continuously in the direction it is facing.  
6. Players can change the direction of the snake using arrow keys (Up, Down, Left, Right).
7. The snake should grow one unit in length when it consumes a food item.
8. The game should end if the snake collides with the walls or its own body.
9. The game should go on endlessly until one of the players presses reset.

Follow the structure provided below and complete the game implementation:"""

context_prompt_code = """

import pygame
import sys
import random


WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)


class SnakeGame:
    def __init__(self):
        pygame.init()
        \"\"\"
        Initialize the game screen, clock, game state, sprites and reset button
        \"\"\"
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.reset_button = pygame.Rect(20, 20, 100, 50)
        self.reset_button_active = False
        

    def reset_game(self):
        \"\"\"
        Reset the game state
        \"\"\"
        

    def update_game_state(self):
        \"\"\"
        Update the game state
        \"\"\"


    def handle_events(self):
        \"\"\"
        Handle events
        \"\"\"
    
    def run(self):
        while True:
            self.handle_events()
            self.update_game_state()
            self.render_game()


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        \"\"\"
        Initialize the snake's body,length direction and image
        \"\"\"
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        



    def change_direction(self, new_direction):
        \"\"\"
        Change the direction of the snake
        \"\"\"
        
    def check_collision(self):
        \"\"\"
        Check whether the snake has collided with the wall or itself
        \"\"\"

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        \"\"\"
        Randomize the position of the food within the grid
        \"\"\"

if __name__ == "__main__":
    game = SnakeGame()
    game.run()

"""
complete_backbone_code = """
import pygame
import sys
import random

# Define constants for the game
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

class Game:
    \"\"\"
    The main class for the Snake game.
    \"\"\"
    def __init__(self):
        \"\"\"
        Initialize the game and its components.
        \"\"\"
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.win_message = False

        self.all_sprites = pygame.sprite.Group()
        self.snake = Snake()
        self.food = Food()
        self.all_sprites.add(self.snake, self.food)

        self.reset_button = pygame.Rect(20, 20, 100, 50)
        self.reset_button_active = False

    def reset_game(self):
        \"\"\"
        Reset the game to its initial state.
        \"\"\"
        pass

    def handle_events(self):
        \"\"\"
        Handle user events like key presses and mouse clicks.
        \"\"\"
        pass

    def update_game_state(self):
        \"\"\"
        Update the game state, including the snake and food.
        \"\"\"
        pass

    def render_game(self):
        \"\"\"
        Render the game on the screen.
        \"\"\"
        pass

    def show_message(self, message, size=36, x=None, y=None):
        \"\"\"
        Display a message on the screen.
        \"\"\"
        pass

    def run(self):
        \"\"\"
        Run the game loop.
        \"\"\"
        while not self.game_over:
            self.handle_events()

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        \"\"\"
        Initialize the snake's body, length, direction and image.
    \"\"\"
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        self.direction = "RIGHT"
        self.body = [(self.rect.x, self.rect.y)]
        self.snake_length = 1

    def reset(self):
        \"\"\"
        Reset the snake to its initial state.
        \"\"\"
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        self.win_message = False

    def update(self):
        \"\"\"
        Update the snake's position and length.
        \"\"\"
        pass

    def change_direction(self, new_direction):
        \"\"\"
        Change the snake's direction.
        \"\"\"
        pass

    def check_collision(self):
        \"\"\"
        Check for collisions, including wall collisions and self-collisions.
        \"\"\"
        pass

    def grow(self):
        \"\"\"
        Increase the length of the snake.
        \"\"\"
        pass

class Food(pygame.sprite.Sprite):
    \"\"\"
    Class representing the food in the game.
    \"\"\"
    def __init__(self):
        \"\"\"
    Initialize the food's position and image.
    \"\"\"
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.randomize_position()

    def randomize_position(self):
        self.rect.topleft = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )
if __name__ == "__main__":
    game = Game()
    game.run()
"""

complete_code_prompt = f"""
Implement the following game using Pygame:

High-level Game Description:
Players control a snake on the screen and guide it to eat food items.
The objective is to grow the snake as long as possible without running into the walls or the snake's own body.

The game should adhere to the following gameplay specifications:
1. The game screen should have a green background.
2. The current score should be displayed on the screen.
3. The game should have a reset button at the bottom of the screen.
4. Food items are represented as small squres on the screen. After each food item is consumed or when the game starts, a new food item should appear at a random location on the screen.
5. The snake should move continuously in the direction it is facing.  
6. Players can change the direction of the snake using arrow keys (Up, Down, Left, Right).
7. The snake should grow one unit in length when it consumes a food item.
8. The game should end if the snake collides with the walls or its own body.
9. The game should go on endlessly until one of the players presses reset.

Follow the structure provided below and complete the game implementation:
{complete_backbone_code}
"""
iterative_prompt = f"""Implement the following game using Pygame:

High-level Game Description:
Players control a snake on the screen and guide it to eat food items.
The objective is to grow the snake as long as possible without running into the walls or the snake's own body.

The game should adhere to the following UI specifications:
Design the game screen with a green background, displaying the score and featuring a reset button at the bottom.
Present the current score visibly on the screen.
Place a reset button at the screen's bottom for players to initiate a game reset.
Depict food items as small squares randomly appearing on the screen for snake consumption.


Follow the structure provided below and complete the game implementation:
{context_prompt_code}
"""

game_specifications = [
    "Generate new food items at random screen locations after consumption or game start.",
    "Facilitate continuous snake movement in the chosen direction.",
    "Update the score display upon the snake consuming food.",
    "Increase the snake's length by one unit after consuming food.",
    "Detect collisions with walls or the snake's body, concluding the game upon detection.",
    "Respond to the reset button press by resetting the game, including score and positions.",
    "Conclude the game if the snake collides with walls or its own body.",
]

iterative_prompt = """feature a snake character as a series of connected squares on the screen.
the snake should be able to move in four directions: up, down, left, and right.
There should be food items randomly placed on the screen for the snake to eat.
When the snake eats a food item, its length should increase, and the player's score should be updated.
The player's score should be displayed at the top-left corner of the screen.
The game should have a grid-based layout where the snake and food move from one grid cell to another.
The snake should start with a default length and grow as it eats food.
The game should end if the snake collides with the screen borders or with its own body.
After a collision, the game should display "Game Over!" and offer the option to restart.
The player can choose to start a new game after a collision.
"""
high_level_description = f"""Implement the following game using Pygame:

High-level Game Description:
Players control a snake on the screen and guide it to eat food items.
The objective is to grow the snake as long as possible without running into the walls or the snake's own body.

The game should adhere to the following UI specifications:
Design the game screen with a green background, displaying the score and featuring a reset button at the bottom.
Present the current score visibly on the screen.
Place a reset button at the screen's bottom for players to initiate a game reset.
Depict food items as small squares randomly appearing on the screen for snake consumption.

```python
import pygame
import sys
import random

# Define constants for the game
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

class Game:
    \"\"\"
    The main class for the Snake game.
    \"\"\"
    def __init__(self):
        \"\"\"
        Initialize the game and its components.
        \"\"\"
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.game_over = False
        self.win_message = False

        self.all_sprites = pygame.sprite.Group()
        self.snake = Snake()
        self.food = Food()
        self.all_sprites.add(self.snake, self.food)

        self.reset_button = pygame.Rect(20, 20, 100, 50)
        self.reset_button_active = False

    def reset_game(self):
        \"\"\"
        Reset the game to its initial state.
        \"\"\"
        pass

    def render_game(self):
        \"\"\"
        Render the game on the screen.
        \"\"\"
        pass

    def show_message(self, message, size=36, x=None, y=None):
        \"\"\"
        Display a message on the screen.
        \"\"\"
        pass

    def run(self):
        \"\"\"
        Run the main game loop.
        \"\"\"
        while not self.game_over:
            self.handle_events()
            self.update_game_state()
            self.render_game()


if __name__ == "__main__":
    game = Game()
    game.run()
"""

iterative_prompts = """
Create a snake character represented as a series of connected pixels or blocks. Initially, the snake should be a single block that moves in a specific direction within the game window.
Allow the player to control the snake's movement using arrow keys. The snake should be able to turn left or right, but it should not be able to move directly backward.
Implement a basic food system where a food item appears randomly on the screen. 
When the snake consumes the food by moving over it, the snake's length increases, and the player earns points.
Introduce a grid-based system for the game window, and ensure that the snake moves one grid unit at a time. The movement should be continuous in the current direction until the player provides new input.
Implement collision detection to check if the snake collides with itself or hits the game window boundaries. When a collision occurs, end the game and display a "Game Over!" message. Stop all in-game motion upon game over.
Incorporate a scoring system, displaying the current score on the screen during gameplay. The score should increase each time the snake consumes food.
Ensure that the game has no predefined end, allowing the snake to continue growing and the difficulty to increase over time. New food items should appear after the snake consumes one.
Provide an option for the player to restart the game after it ends. Display a "Restart" option on the game over screen to allow the player to play again."""
