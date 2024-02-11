import pygame
import sys
import random
import math


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.screen_width = 800
        self.screen_height = 600
        self.agent_position = {"x": 100, "y": 250}
        self.agent_velocity = {"x": 0, "y": 0}
        self.green_dot_position = {"x": 400, "y": 300}
        self.red_puck_position = {"x": 700, "y": 300}
        self.puck_velocity = 1
        self.thruster_force = 5
        self.decay_factor = 0.95
        self.game_over = False

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()


def render(state_manager):
    state_manager.screen.fill((255, 255, 255))  # Fill the screen with white

    pygame.draw.circle(
        state_manager.screen,
        (0, 0, 255),
        (
            state_manager.agent_position["x"],
            state_manager.agent_position["y"],
        ),
        20,
    )
    pygame.draw.circle(
        state_manager.screen,
        (0, 255, 0),
        (
            state_manager.green_dot_position["x"],
            state_manager.green_dot_position["y"],
        ),
        10,
    )
    pygame.draw.circle(
        state_manager.screen,
        (255, 0, 0),
        (
            state_manager.red_puck_position["x"],
            state_manager.red_puck_position["y"],
        ),
        50,
    )

    pygame.display.flip()
    state_manager.clock.tick(60)


def agent_movement_logic(state_manager, action):
    # Apply thrusters based on action
    if action == "up":
        state_manager.agent_velocity["y"] -= state_manager.thruster_force
    elif action == "down":
        state_manager.agent_velocity["y"] += state_manager.thruster_force
    elif action == "left":
        state_manager.agent_velocity["x"] -= state_manager.thruster_force
    elif action == "right":
        state_manager.agent_velocity["x"] += state_manager.thruster_force

    # Update agent position based on velocity
    state_manager.agent_position["x"] += state_manager.agent_velocity["x"]
    state_manager.agent_position["y"] += state_manager.agent_velocity["y"]

    # Decay agent velocity over time
    state_manager.agent_velocity["x"] *= state_manager.decay_factor
    state_manager.agent_velocity["y"] *= state_manager.decay_factor


def puck_movement_logic(state_manager):
    # Move the red puck towards the agent
    angle = math.atan2(
        state_manager.agent_position["y"] - state_manager.red_puck_position["y"],
        state_manager.agent_position["x"] - state_manager.red_puck_position["x"],
    )
    state_manager.red_puck_position["x"] += state_manager.puck_velocity * math.cos(
        angle
    )
    state_manager.red_puck_position["y"] += state_manager.puck_velocity * math.sin(
        angle
    )


def collision_logic(state_manager):
    # Check for collision with the green dot
    distance = math.sqrt(
        (state_manager.agent_position["x"] - state_manager.green_dot_position["x"]) ** 2
        + (state_manager.agent_position["y"] - state_manager.green_dot_position["y"])
        ** 2
    )
    if distance < 20:
        state_manager.game_over = True

    # Check for collision with the red puck
    distance = math.sqrt(
        (state_manager.agent_position["x"] - state_manager.red_puck_position["x"]) ** 2
        + (state_manager.agent_position["y"] - state_manager.red_puck_position["y"])
        ** 2
    )
    if distance < 30:
        state_manager.game_over = True


def game_over_logic(state_manager):
    # Handle game over logic
    if state_manager.game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        state_manager.screen.blit(game_over_text, (250, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()


def main():
    pygame.init()
    state_manager = StateManager()

    running = True
    while running:
        action = pygame.event.poll()

        if action.type == pygame.QUIT:
            running = False

        if action.type == pygame.KEYDOWN and not state_manager.game_over:
            if action.key == pygame.K_UP:
                agent_movement_logic(state_manager, "up")
            elif action.key == pygame.K_DOWN:
                agent_movement_logic(state_manager, "down")
            elif action.key == pygame.K_LEFT:
                agent_movement_logic(state_manager, "left")
            elif action.key == pygame.K_RIGHT:
                agent_movement_logic(state_manager, "right")

        # Environment logic
        puck_movement_logic(state_manager)
        collision_logic(state_manager)
        game_over_logic(state_manager)

        # UI rendering
        render(state_manager)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("PuckWorld")
    main()
