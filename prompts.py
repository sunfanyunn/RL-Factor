state_change_prompt = """The game designer is building a single-player game in Pygame by modeling this game as a Markov Decision Process (MDP).
Your task is to identify and compile a list of relevant state variables to implement a specific feature requested by the game designer.
The game already has the following state space implementation:
```python
import pygame
import sys
import random


{state_manager_code}

    # new variables will be added here:
    # variable_description
    self.{{variable_name}} = {{variable_type}}({{value}})
```

Please provide the state variables in the following format within a JSON object:
```json
{{
    "state_variables": [
        {{
            "variable_description": "Description of the variable",
            "variable_name": "Name of the variable",
            "variable_type": "Type of the variable, one of {{int, float, str, bool, tuple, list}}",
            "variable_value": "Value of the variable, e.g. 100, 0.5, 'balloon', tuple((255, 0, 255)), True, [10, 50], [{{'x': 100, 'y': 200}}]",
        }},
        ...
    ]
}}
```

The game designer's request is: {query}.
Here are the dos and don'ts for this request:
- Additionally, you may add new state variables if necessary, but prioritize reusing the existing state variables as much as possible. For example, if we have "position_x" and "position_y" of the protagonist character, do not give me another variable "positions" in a list format.
- Please return a single list of state variables that contains both existing variables that you think are relevant and new state variables.
- A software engineer will later implement this request by implementing a function that takes these variables as input, so ensure all the variables needed to implement the request are included.
- It is okay to include variables that don't end up being used in the implementation because redundant state variables will be filtered out later.
- Please provide all rendering variables (e.g., size, color) if there are components to be rendered. Color should never be white since the background is white.
- Don't provide Sprite, Surface, or Rect variables. We will handle these variables later.
- Don't introduce variables using existing variables (e.g., self.bird_size = self.pipe_size/2), all state variables should be independent of each other.
- Always provide a default value even if a state variable should be chosen randomly. The randomness will be implemented later.
- "variable_value" should never to empty like []. Always provide a non-empty default value so the software engineer can infer how the variable can be accessed.
"""

decompose_query_prompt = """The game designer is building a single-player game in Pygame by modeling this game as a Markov Decision Process (MDP).
There are three types of functions/modules in this game: input event handling, state transition, and UI rendering. 
- input event handling: functions that detect user input and update the state variables accordingly.
- state transition: functions that update the state variables according to the game logic.
- UI rendering: functions that render the state variables as UI components on the screen.

Given a specific feature requested by the game designer, your task is to decide how to implement this feature by decomposing it into the three types of functions/modules mentioned above.

The game already has the following implementation:
```python
import pygame
import sys
import random


{state_manager_code}

# all the input event handling functions
{relevant_input_def}

# all the state transitional functions
{relevant_logic_def}

# all the UI rendering functions that govern how state variables are rendered as UI components
{relevant_render_def}

def main():
    state_manager = StateManager()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        # call all the input event handling functions
        # call all the state transitional functions
        # call all the rendering functions
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    main()
```

Please provide the answer in the following format within a JSON object:
```json
{{
    "input_logic": {{
        "description": "the detailed description of what this function should achieve.",
        "function_name": "the name of the function to be added",
    }},
    "state_transition": {{
        "description": "the detailed description of what this function should achieve",
        "function_name": "the name of the function to be added",
    }},
    "ui_rendering": {{
        "description": "the detailed description of what this function should achieve",
        "function_name": "the name of the function to be added",
    }},
   
}}
```

The game designer's request is: {query}.

Here are the dos and don'ts for this request:
- Only give output that pertains to the particular request from the game designer. Do not add things that are not requested. For example, if the game designer asks to "introduce an obstacle", do not add additional logics such as "allow the human player to control the obstacle with arrow keys".
- Be detailed and specific about what the function should achieve. For example, do not give instructions such as "description": "This function should handle input events relevant to the game.".
- The resulting JSON should have three keys: "input_logic", "state_transition", and "ui_rendering". Each key should have two keys: "description" and "function_name". The "description" key should have a string value that describes what the function should achieve. The "function_name" key should have a string value that is the name of the function to be added. If the function already exists, this new function will be used in place of the old one.
- If any particular type of functions is not needed, please leave it as an empty string. It is okay to have empty strings if the function has already been implemented.
- The state variables are already updated according to the game designer's request. You should not include steps that update the state variables.
"""

input_logic_add_prompt = """The game designer is building a single-player game in Pygame by modeling this game as a Markov Decision Process (MDP). Your task is to detect key/mouse input and update the state variables accordingly according to a feature requested by the game designer.
The game has the following implementation already:
```python
import pygame
import sys
import random


{state_manager_code}

# the new logic function will be here
{existing_implementation}

def main():
    state_manager = StateManager()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        # {{function_description}}
        {{function_name}}(state_manager, event)
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    main()
```

Please implement the following request from the game designer and return your answer in the following format:
```json
{{
    "function_name": "{function_name}",
    "function_description": "{function_description}",
    "function_implementation": "the pygame implementation of the function, including the first line of the function definition",
}}
```

Here are the dos and don'ts for this request:
- Note that the implementation of the function shuold only have two arguments (i.e. state_manager and event).
- The function implementation should involve checking user input with event (i.e. event.type and event.key).
- Minimize the number of functions added while meeting the game designer's requirements. However, make sure to always give the full implementation of the function.
- Include only the essential details requested by the game designer. Do not add things that are not requested.
"""

logic_add_prompt = """The game designer is building a single-player game in Pygame by modeling this game as a Markov Decision Process (MDP). Your task is to define and code new state transition functions according to the feature requested by the game designer.
The game has the following implementation already:
```python
import pygame
import sys
import random


{state_manager_code}

# the new function will be here
{existing_implementation}


def main():
    state_manager = StateManager()
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        # {{function_description}}
        {{function_name}}(state_manager)
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    main()
```

Please implement the following request from the game designer and return your answer in the following format:
```json
{{
    "function_name": "{function_name}",
    "function_description": "{function_description}",
    "function_implementation": "the pygame implementation of the function, including the first line of the function definition",
}}
```

Here are the dos and don'ts for this request:
- Only implement things that pertain to updating the state variables. Other aspects of the game like input event handling and UI components will be handled separately.
- Minimize the number of functions added while meeting the game designer's requirements.
- Include only the essential details requested by the game designer. Do not add things that are not requested.
- These state transition functions will be called in every iteration of the main game loop. If you want to add a conditional logic to the function, please implement it in the function itself.
- Note that the new function will be added to the end of the list of state transition functions.
"""

ui_add_prompt = """The game designer is building a single-player game in Pygame by modeling this game as a Markov Decision Process (MDP). Your task is to add rendering functions that decide how state variables are rendered as UI components on the screen, according to the feature requested by the game designer.
The game has the following implementation already:
```python
import pygame
import sys
import random


{state_manager_code}

# all the code for the rendering functions
{render_code}
# the new rendering function will be here

def main():
    state_manager = StateManager()
    clock = pygame.time.Clock()
    running = True
    while running:
        action = pygame.event.poll()
        if action.type == pygame.QUIT:
            running = False

        # all the code for state transitional logics
        # omitted for brevity

        # Fill the screen with white
        state_manager.screen.fill((255, 255, 255))
        # all the code for rendering states as UI components
        # {{function_description}}
        {{function_name}}(state_manager)
        pygame.display.flip()
        state_manager.clock.tick(state_manager.fps)

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("")
    main()
```

Please implement the following request from the game designer and return your answer in the following format:
```json
{{
    "function_name": "{function_name}",
    "function_description": "{function_description}",
    "function_implementation": "the pygame implementation of the function, including the first line of the function definition",
}}
```

Here are the dos and don'ts for this request:
- Only implement things that pertain to how state variables are rendered as UI components on the screen. Other aspects like input event handling and state transition will be handled separately.
- Please make sure that all of the state variables remain unchanged in the rendering functions.
- Minimize the number of functions to add while meeting the game designer's requirements.
- Include only the essential details requested by the game designer. Do not add things that are not requested.
- These rendering functions will be called in every iteration of the main game loop. If you want to add a conditional logic to the function, please implement it in the function itself.
- Note that the background color of the screen is white so white UI components will not be visible. Do not fill the screen with white again in the rendering functions.
- Note that the new function will be added to the end of the list of rendering functions.
"""
