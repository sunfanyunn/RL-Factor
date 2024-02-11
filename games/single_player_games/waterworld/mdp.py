import pygame
import sys
import random
import math


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.screen_height = 600
        self.screen_width = 800
        self.player_position = {"x": 100, "y": 300}
        self.player_velocity = {"x": 0, "y": 0}
        self.thruster_power = 2
        self.thruster_decay = 0.1
        self.score = 0
        self.game_over = False
        self.circles = []

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()


def render(state_manager):
    state_manager.screen.fill((0, 0, 255))  # Fill the screen with blue for water

    # Render player
    pygame.draw.circle(
        state_manager.screen,
        (0, 255, 255),
        (
            int(state_manager.player_position["x"]),
            int(state_manager.player_position["y"]),
        ),
        20,
    )

    # Render circles
    for circle in state_manager.circles:
        color = (0, 255, 0) if circle["color"] == "green" else (255, 0, 0)
        pygame.draw.circle(
            state_manager.screen,
            color,
            (int(circle["x"]), int(circle["y"])),
            15,
        )

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {state_manager.score}", True, (255, 255, 255))
    state_manager.screen.blit(score_text, (10, 10))

    pygame.display.flip()
    state_manager.clock.tick(60)


def player_logic(state_manager):
    """Apply thrusters, update velocity, and update position for the player."""
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        state_manager.player_velocity["y"] -= state_manager.thruster_power
    if keys[pygame.K_DOWN]:
        state_manager.player_velocity["y"] += state_manager.thruster_power
    if keys[pygame.K_LEFT]:
        state_manager.player_velocity["x"] -= state_manager.thruster_power
    if keys[pygame.K_RIGHT]:
        state_manager.player_velocity["x"] += state_manager.thruster_power

    # Decay player velocity over time
    state_manager.player_velocity["x"] *= 1 - state_manager.thruster_decay
    state_manager.player_velocity["y"] *= 1 - state_manager.thruster_decay

    # Update player position based on velocity
    state_manager.player_position["x"] += state_manager.player_velocity["x"]
    state_manager.player_position["y"] += state_manager.player_velocity["y"]

    # Keep player within screen boundaries
    state_manager.player_position["x"] = max(
        0, min(state_manager.player_position["x"], state_manager.screen_width - 20)
    )
    state_manager.player_position["y"] = max(
        0, min(state_manager.player_position["y"], state_manager.screen_height - 20)
    )


def circle_logic(state_manager):
    """Move the circles and update the score."""
    captured_circles = [
        circle for circle in state_manager.circles if circle["captured"]
    ]
    for captured_circle in captured_circles:
        state_manager.circles.remove(captured_circle)

        # Respawn the circle in a random location as either red or green
        new_circle = {
            "x": random.randint(50, state_manager.screen_width - 50),
            "y": random.randint(50, state_manager.screen_height - 50),
            "color": random.choice(["red", "green"]),
            "captured": False,
            "velocity_x": random.uniform(-2, 2),
            "velocity_y": random.uniform(-2, 2),
        }
        state_manager.circles.append(new_circle)

    # Move circles smoothly
    for circle in state_manager.circles:
        # Check if the velocity keys exist in the dictionary
        if "velocity_x" not in circle:
            circle["velocity_x"] = random.uniform(-2, 2)
        if "velocity_y" not in circle:
            circle["velocity_y"] = random.uniform(-2, 2)

        # Update circle position based on velocity
        circle["x"] += circle["velocity_x"]
        circle["y"] += circle["velocity_y"]

        # Keep circles within screen boundaries
        circle["x"] = max(30, min(circle["x"], state_manager.screen_width - 30))
        circle["y"] = max(30, min(circle["y"], state_manager.screen_height - 30))

    player_rect = pygame.Rect(
        state_manager.player_position["x"],
        state_manager.player_position["y"],
        20,
        20,
    )

    # Check for collision with circles and update captured status
    for circle in state_manager.circles:
        circle_rect = pygame.Rect(
            circle["x"],
            circle["y"],
            30,
            30,
        )

        if player_rect.colliderect(circle_rect) and not circle["captured"]:
            circle["captured"] = True
            if circle["color"] == "green":
                state_manager.score += 1
            else:
                state_manager.score -= 1

    # Update the list of green circles
    green_circles = [
        circle
        for circle in state_manager.circles
        if circle["color"] == "green" and not circle["captured"]
    ]

    # Check if all green circles have been captured
    if len(green_circles) == 0:
        state_manager.game_over = True


def game_over_logic(state_manager):
    """Handle game over logic"""
    if state_manager.game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        state_manager.screen.blit(game_over_text, (250, 250))
        pygame.display.flip()

        # Wait for a key press to start a new game
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # You can use any key you prefer
                        waiting_for_key = False
            pygame.time.delay(100)  # Small delay to avoid high CPU usage

        reset_game(state_manager)


def reset_game(state_manager):
    """Reset the game state for a new game."""
    state_manager.player_position = {"x": 100, "y": 300}
    state_manager.player_velocity = {"x": 0, "y": 0}
    state_manager.score = 0
    state_manager.game_over = False
    state_manager.circles = []

    # Initialize circles for a new game
    for _ in range(10):
        new_circle = {
            "x": random.randint(50, state_manager.screen_width - 50),
            "y": random.randint(50, state_manager.screen_height - 50),
            "color": random.choice(["red", "green"]),
            "captured": False,
        }
        state_manager.circles.append(new_circle)


def main():
    pygame.init()
    state_manager = StateManager()

    # Initialize circles
    for _ in range(10):
        new_circle = {
            "x": random.randint(50, state_manager.screen_width - 50),
            "y": random.randint(50, state_manager.screen_height - 50),
            "color": random.choice(["red", "green"]),
            "captured": False,
        }
        state_manager.circles.append(new_circle)

    running = True
    while running:
        action = pygame.event.poll()

        if action.type == pygame.QUIT:
            running = False

        player_logic(state_manager)
        circle_logic(state_manager)
        game_over_logic(state_manager)
        render(state_manager)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("WaterWorld")
    main()
