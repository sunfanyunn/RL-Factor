import pygame
import sys
import random


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.screen_width = 800
        self.screen_height = 600
        self.copter_position = {"x": 100, "y": 250}
        self.gravity = 2
        self.jump_velocity = -30
        self.score = 0
        self.game_over = False
        self.obstacle_gap = 200
        self.obstacle_width = 50
        self.obstacle_positions = []

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()


def render(state_manager):
    state_manager.screen.fill((255, 255, 255))

    pygame.draw.rect(
        state_manager.screen,
        (0, 255, 0),
        (
            state_manager.copter_position["x"],
            state_manager.copter_position["y"],
            30,
            30,
        ),
    )

    for obstacle in state_manager.obstacle_positions:
        pygame.draw.rect(
            state_manager.screen,
            (255, 0, 0),
            (obstacle["x"], 0, state_manager.obstacle_width, obstacle["gap_y"]),
        )
        pygame.draw.rect(
            state_manager.screen,
            (255, 0, 0),
            (
                obstacle["x"],
                obstacle["gap_y"] + state_manager.obstacle_gap,
                state_manager.obstacle_width,
                state_manager.screen_height,
            ),
        )

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {state_manager.score}", True, (0, 0, 0))
    state_manager.screen.blit(score_text, (10, 10))

    pygame.display.flip()
    state_manager.clock.tick(60)


def gravity_logic(state_manager):
    state_manager.copter_position["y"] += state_manager.gravity


def jump_logic(state_manager):
    state_manager.copter_position["y"] += state_manager.jump_velocity


def obstacle_logic(state_manager):
    max_obstacles_on_screen = 3

    copter_rect = pygame.Rect(
        state_manager.copter_position["x"],
        state_manager.copter_position["y"],
        30,
        30,
    )

    for obstacle in state_manager.obstacle_positions:
        obstacle["x"] -= 5

        obstacle_rect_upper = pygame.Rect(
            obstacle["x"], 0, state_manager.obstacle_width, obstacle["gap_y"]
        )
        obstacle_rect_lower = pygame.Rect(
            obstacle["x"],
            obstacle["gap_y"] + state_manager.obstacle_gap,
            state_manager.obstacle_width,
            state_manager.screen_height,
        )

        if (
            copter_rect.colliderect(obstacle_rect_upper)
            or copter_rect.colliderect(obstacle_rect_lower)
            or state_manager.copter_position["y"] < 0
            or state_manager.copter_position["y"] >= state_manager.screen_height
        ):
            state_manager.game_over = True

        if (
            not obstacle["counted"]
            and state_manager.copter_position["x"] > obstacle["x"]
        ):
            state_manager.score += 1
            obstacle["counted"] = True

    # Remove obstacles that are out of the screen
    state_manager.obstacle_positions = [
        obstacle
        for obstacle in state_manager.obstacle_positions
        if obstacle["x"] + state_manager.obstacle_width > 0
    ]

    # Add new obstacles with aligned gaps
    while len(state_manager.obstacle_positions) < max_obstacles_on_screen:
        last_obstacle = (
            state_manager.obstacle_positions[-1]
            if state_manager.obstacle_positions
            else None
        )
        new_obstacle_x = (
            last_obstacle["x"] + state_manager.obstacle_width
            if last_obstacle
            else state_manager.screen_width
        )

        gap_y = random.randint(
            50,
            state_manager.screen_height - state_manager.obstacle_gap - 50,
        )
        new_obstacle = {
            "x": new_obstacle_x,
            "gap_y": gap_y,
            "counted": False,
        }
        state_manager.obstacle_positions.append(new_obstacle)

        # Add obstacles with aligned gaps
        for _ in range(1, 3):
            new_obstacle_x += state_manager.obstacle_width
            new_obstacle = {
                "x": new_obstacle_x,
                "gap_y": gap_y,
                "counted": False,
            }
            state_manager.obstacle_positions.append(new_obstacle)


def game_over_logic(state_manager):
    if state_manager.game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        state_manager.screen.blit(game_over_text, (250, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    if state_manager.copter_position["y"] >= state_manager.screen_height:
        state_manager.game_over = True


def main():
    pygame.init()
    state_manager = StateManager()

    running = True
    while running:
        action = pygame.event.poll()

        if action.type == pygame.QUIT:
            running = False

        if action.type == pygame.MOUSEBUTTONDOWN and not state_manager.game_over:
            jump_logic(state_manager)

        gravity_logic(state_manager)
        obstacle_logic(state_manager)
        game_over_logic(state_manager)
        render(state_manager)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pixelcopter")
    main()
