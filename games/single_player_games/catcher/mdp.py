import pygame
import sys
import random


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.screen = pygame.display.set_mode((1000, 1000))
        self.screen_width = 1000
        self.screen_height = 1000
        self.fruit_radius = 10
        self.catcher_position_x = 180
        self.catcher_position_y = 950
        self.catcher_width = 50
        self.catcher_height = 50

        self.balls = [{"x": 200, "y": 0}]
        self.game_over = False
        self.score = 0
        self.lives = 3

        self.clock = pygame.time.Clock()


def render(state_manager):
    state_manager.screen.fill((255, 255, 255))  # Fill the screen with white

    pygame.draw.rect(
        state_manager.screen,
        (0, 255, 0),
        pygame.Rect(
            state_manager.catcher_position_x,
            state_manager.catcher_position_y,
            state_manager.catcher_width,
            state_manager.catcher_height,
        ),
    )

    # Render fruits
    fruit_radius = 10
    for fruit in state_manager.balls:
        pygame.draw.circle(
            state_manager.screen,
            (255, 0, 0),
            (fruit["x"], fruit["y"]),
            fruit_radius,
        )

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {state_manager.score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {state_manager.lives}", True, (0, 0, 0))
    state_manager.screen.blit(score_text, (10, 10))
    state_manager.screen.blit(lives_text, (state_manager.screen_height - 100, 10))

    pygame.display.flip()
    state_manager.clock.tick(60)


def catcher_movement_logic(state_manager, event):
    """Move the catcher based on the user's input."""
    if not state_manager.game_over:
        action = ""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action = "LEFT"
            elif event.key == pygame.K_RIGHT:
                action = "RIGHT"

        if action == "LEFT" and state_manager.catcher_position_x > 0:
            state_manager.catcher_position_x -= 20
        elif (
            action == "RIGHT"
            and state_manager.catcher_position_x
            < state_manager.screen_width - state_manager.catcher_width
        ):
            state_manager.catcher_position_x += 20


def fruit_logic(state_manager):
    """Move the fruits down and check for catching."""
    max_fruits_on_screen = 1

    catcher_rect = pygame.Rect(
        state_manager.catcher_position_x,
        state_manager.catcher_position_y,
        state_manager.catcher_width,
        state_manager.catcher_height,
    )

    for fruit in state_manager.balls:
        fruit["y"] += 5

        # Check for catching the fruit
        fruit_rect = pygame.Rect(
            fruit["x"],
            fruit["y"],
            2 * state_manager.fruit_radius,
            2 * state_manager.fruit_radius,
        )

        if catcher_rect.colliderect(fruit_rect):
            state_manager.score += 1
            state_manager.balls.remove(fruit)
        elif fruit["y"] >= state_manager.screen_height:
            state_manager.lives -= 1

    # Remove fruits that are out of the screen
    state_manager.balls = [
        fruit
        for fruit in state_manager.balls
        if fruit["y"] < state_manager.screen_height
    ]

    # Add new fruit
    if (
        random.randint(1, 100) <= 10
        and len(state_manager.balls) < max_fruits_on_screen
    ):
        new_fruit = {
            "x": random.randint(0, state_manager.screen_width),
            "y": 0,
        }
        state_manager.balls.append(new_fruit)


def game_over_logic(state_manager):
    """Handle game over logic"""
    if state_manager.lives <= 0:
        state_manager.game_over = True

    if state_manager.game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        state_manager.screen.blit(game_over_text, (100, 150))
        state_manager.__init__()


class Game():
    def __init__(self):
        self.state_manager = StateManager()
        self.state_manager.screen = pygame.display.set_mode((self.state_manager.screen_width,
                                                             self.state_manager.screen_height))

    def run(self, event):
        state_manager = self.state_manager
        catcher_movement_logic(state_manager, event)
        fruit_logic(state_manager)

        # Check for missed fruits and decrease lives
        if (
            state_manager.balls
            and state_manager.balls[0]["y"] >= state_manager.screen_height
        ):
            state_manager.lives -= 1
            state_manager.balls = []

        game_over_logic(state_manager)
        render(state_manager)
        return True

if __name__ == "__main__":
    game = Game()
    pygame.init()
    global event
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()