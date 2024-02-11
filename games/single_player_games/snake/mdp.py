import pygame
import sys
import random


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.screen_width = 600
        self.screen_height = 400
        self.snake_segments = [{"x": 100, "y": 100}]
        self.snake_direction = "RIGHT"
        self.food_position = {"x": 200, "y": 200}
        self.score = 0
        self.game_over = False

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()


def render(state_manager):
    state_manager.screen.fill((255, 255, 255))  # Fill the screen with white

    # Render snake
    for segment in state_manager.snake_segments:
        pygame.draw.rect(
            state_manager.screen,
            (0, 255, 0),
            (segment["x"], segment["y"], 20, 20),
        )

    # Render food
    pygame.draw.rect(
        state_manager.screen,
        (255, 0, 0),
        (
            state_manager.food_position["x"],
            state_manager.food_position["y"],
            20,
            20,
        ),
    )

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {state_manager.score}", True, (0, 0, 0))
    state_manager.screen.blit(score_text, (10, 10))

    pygame.display.flip()
    state_manager.clock.tick(10)


def snake_logic(state_manager):
    # Move the snake in the current direction
    head = state_manager.snake_segments[0].copy()

    if state_manager.snake_direction == "UP":
        head["y"] -= 20
    elif state_manager.snake_direction == "DOWN":
        head["y"] += 20
    elif state_manager.snake_direction == "LEFT":
        head["x"] -= 20
    elif state_manager.snake_direction == "RIGHT":
        head["x"] += 20

    # Check for collisions with walls or itself
    if (
        head["x"] < 0
        or head["x"] >= state_manager.screen_width
        or head["y"] < 0
        or head["y"] >= state_manager.screen_height
        or head in state_manager.snake_segments[1:]
    ):
        state_manager.game_over = True

    # Check for collisions with food
    if head == state_manager.food_position:
        state_manager.score += 1
        state_manager.food_position = {
            "x": random.randint(0, state_manager.screen_width // 20 - 1) * 20,
            "y": random.randint(0, state_manager.screen_height // 20 - 1) * 20,
        }
    else:
        # Move the snake by adding a new head and removing the tail
        state_manager.snake_segments.insert(0, head)
        state_manager.snake_segments = state_manager.snake_segments[
            : state_manager.score + 1
        ]


def game_over_logic(state_manager):
    if state_manager.game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        state_manager.screen.blit(game_over_text, (150, 200))
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
            if action.key == pygame.K_UP and state_manager.snake_direction != "DOWN":
                state_manager.snake_direction = "UP"
            elif action.key == pygame.K_DOWN and state_manager.snake_direction != "UP":
                state_manager.snake_direction = "DOWN"
            elif (
                action.key == pygame.K_LEFT and state_manager.snake_direction != "RIGHT"
            ):
                state_manager.snake_direction = "LEFT"
            elif (
                action.key == pygame.K_RIGHT and state_manager.snake_direction != "LEFT"
            ):
                state_manager.snake_direction = "RIGHT"

        snake_logic(state_manager)
        game_over_logic(state_manager)
        render(state_manager)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Snake Game")
    main()
