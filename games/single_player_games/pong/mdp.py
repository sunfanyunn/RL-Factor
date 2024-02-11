import pygame
import sys
import random


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.screen_width = 800
        self.screen_height = 600
        self.paddle_width = 20
        self.paddle_height = 100
        self.ball_radius = 10
        self.ball_speed = 5
        self.player_paddle = {"x": 50, "y": 250}
        self.cpu_paddle = {"x": 730, "y": 250, "speed": 2}
        self.ball = {"x": 400, "y": 300, "speed_x": 5, "speed_y": 2}
        self.player_score = 0
        self.cpu_score = 0
        self.game_over = False

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()


def render(state_manager):
    state_manager.screen.fill((255, 255, 255))  # Fill the screen with white

    # Render paddles
    pygame.draw.rect(
        state_manager.screen,
        (0, 0, 255),
        (
            state_manager.player_paddle["x"],
            state_manager.player_paddle["y"],
            state_manager.paddle_width,
            state_manager.paddle_height,
        ),
    )

    pygame.draw.rect(
        state_manager.screen,
        (255, 0, 0),
        (
            state_manager.cpu_paddle["x"],
            state_manager.cpu_paddle["y"],
            state_manager.paddle_width,
            state_manager.paddle_height,
        ),
    )

    # Render ball
    pygame.draw.circle(
        state_manager.screen,
        (0, 255, 0),
        (state_manager.ball["x"], state_manager.ball["y"]),
        state_manager.ball_radius,
    )

    # Render scores
    font = pygame.font.Font(None, 36)
    player_score_text = font.render(
        f"Player: {state_manager.player_score}", True, (0, 0, 0)
    )
    cpu_score_text = font.render(f"CPU: {state_manager.cpu_score}", True, (0, 0, 0))
    state_manager.screen.blit(player_score_text, (50, 10))
    state_manager.screen.blit(cpu_score_text, (state_manager.screen_width - 150, 10))

    pygame.display.flip()
    state_manager.clock.tick(60)


def move_paddle_up(paddle):
    paddle["y"] -= 10


def move_paddle_down(paddle):
    paddle["y"] += 10


def ball_movement(state_manager):
    state_manager.ball["x"] += state_manager.ball["speed_x"]
    state_manager.ball["y"] += state_manager.ball["speed_y"]

    # Ball-wall collision
    if (
        state_manager.ball["y"] - state_manager.ball_radius <= 0
        or state_manager.ball["y"] + state_manager.ball_radius
        >= state_manager.screen_height
    ):
        state_manager.ball["speed_y"] = -state_manager.ball["speed_y"]

    # Ball-paddle collision
    if (
        state_manager.ball["x"] - state_manager.ball_radius
        <= state_manager.player_paddle["x"] + state_manager.paddle_width
        and state_manager.player_paddle["y"]
        <= state_manager.ball["y"]
        <= state_manager.player_paddle["y"] + state_manager.paddle_height
    ):
        state_manager.ball["speed_x"] = abs(state_manager.ball["speed_x"])

        # Update player score when the ball hits the player's paddle
        state_manager.player_score += 1

    if (
        state_manager.ball["x"] + state_manager.ball_radius
        >= state_manager.cpu_paddle["x"]
        and state_manager.cpu_paddle["y"]
        <= state_manager.ball["y"]
        <= state_manager.cpu_paddle["y"] + state_manager.paddle_height
    ):
        state_manager.ball["speed_x"] = -abs(state_manager.ball["speed_x"])

        # Update CPU score when the ball hits the CPU's paddle
        state_manager.cpu_score += 1


def cpu_logic(state_manager):

    if (
        state_manager.ball["y"]
        < state_manager.cpu_paddle["y"] + state_manager.paddle_height / 2
    ):
        state_manager.cpu_paddle["speed"] = -abs(state_manager.cpu_paddle["speed"])
    else:
        state_manager.cpu_paddle["speed"] = abs(state_manager.cpu_paddle["speed"])

    state_manager.cpu_paddle["y"] += state_manager.cpu_paddle["speed"]


def game_over_logic(state_manager):
    if state_manager.ball["x"] < 0:
        state_manager.game_over = True

    if state_manager.game_over:
        font = pygame.font.Font(None, 72)
        winner_text = font.render(
            "Player Wins!"
            if state_manager.player_score > state_manager.cpu_score
            else "CPU Wins!",
            True,
            (0, 0, 0),
        )
        state_manager.screen.blit(winner_text, (250, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()


def main():
    pygame.init()
    state_manager = StateManager()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and state_manager.player_paddle["y"] > 0:
            move_paddle_up(state_manager.player_paddle)
        if (
            keys[pygame.K_DOWN]
            and state_manager.player_paddle["y"]
            < state_manager.screen_height - state_manager.paddle_height
        ):
            move_paddle_down(state_manager.player_paddle)

        # Update game state
        cpu_logic(state_manager)
        ball_movement(state_manager)
        game_over_logic(state_manager)

        # Render game
        render(state_manager)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pong")
    main()
