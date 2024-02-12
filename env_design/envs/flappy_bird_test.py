import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
import random


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.SCREEN_WIDTH = 240
        self.SCREEN_HEIGHT = 320
        self.PIPE_WIDTH = 10
        self.PIPE_GAP = 50

        self.bird_position_x = 100
        self.bird_position_y = 150
        self.bird_size = 10
        self.score = 0
        self.pipe_positions = [{"x": 480, "y": 100, "counted": False}]

        self.jump_velocity = -30
        self.gravity = 1
        self.game_over = False

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()


def render(state_manager):
    state_manager.screen.fill((255, 255, 255))  # Fill the screen with white

    pygame.draw.circle(
        state_manager.screen,
        (255, 0, 0),
        (state_manager.bird_position_x, state_manager.bird_position_y),
        state_manager.bird_size,
    )

    # Render pipes
    for pipe in state_manager.pipe_positions:
        pygame.draw.rect(
            state_manager.screen,
            (0, 0, 255),
            (
                pipe["x"],
                pipe["y"],
                state_manager.PIPE_WIDTH,
                state_manager.SCREEN_HEIGHT - pipe["y"],
            ),
        )

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {state_manager.score}", True, (0, 0, 0))
    state_manager.screen.blit(score_text, (10, 10))

    pygame.display.update()
    state_manager.clock.tick(60)


def gravity_logic(state_manager):
    state_manager.bird_position_y += state_manager.gravity


def jump_logic(state_manager, event):
    if event.type == pygame.MOUSEBUTTONDOWN and not state_manager.game_over:
        state_manager.bird_position_y += state_manager.jump_velocity


def pipe_logic(state_manager):
    max_pipes_on_screen = 3

    bird_rect = pygame.Rect(
        state_manager.bird_position_x,
        state_manager.bird_position_y,
        state_manager.bird_size,
        state_manager.bird_size,
    )

    for pipe in state_manager.pipe_positions:
        pipe["x"] -= 1

        # Check for collision with pipes
        pipe_rect = pygame.Rect(
            pipe["x"],
            pipe["y"],
            state_manager.PIPE_WIDTH,
            state_manager.SCREEN_HEIGHT - pipe["y"],
        )

        if (
            bird_rect.colliderect(pipe_rect)
            or state_manager.bird_position_y < 0
            or state_manager.bird_position_y >= state_manager.SCREEN_HEIGHT
        ):
            state_manager.game_over = True

        # Check if the bird passed through the pipe
        if not pipe["counted"] and state_manager.bird_position_x > pipe["x"]:
            state_manager.score += 1
            pipe["counted"] = True

    # Remove pipes that are out of the screen
    state_manager.pipe_positions = [
        pipe
        for pipe in state_manager.pipe_positions
        if pipe["x"] + state_manager.PIPE_WIDTH > 0
    ]

    # Add new pipes
    if (
        random.randint(1, 100) <= 10
        and len(state_manager.pipe_positions) < max_pipes_on_screen
    ):
        new_pipe = {
            "x": state_manager.SCREEN_WIDTH,
            "y": random.randint(
                50,
                state_manager.SCREEN_HEIGHT- state_manager.PIPE_GAP - 50,
            ),
            "counted": False,
        }
        state_manager.pipe_positions.append(new_pipe)

        for _ in range(4):
            new_pipe = {
                "x": new_pipe["x"] + 250,
                "y": random.randint(
                    50,
                    state_manager.SCREEN_HEIGHT - state_manager.PIPE_GAP - 50,
                ),
                "counted": False,
            }
            state_manager.pipe_positions.append(new_pipe)


def game_over_logic(state_manager):
    if state_manager.bird_position_y <= 0:
        state_manager.game_over = True
    if state_manager.bird_position_y >= state_manager.SCREEN_HEIGHT:
        state_manager.game_over = True

    if state_manager.game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        state_manager.screen.blit(game_over_text, (250, 250))
        pygame.display.flip()
        pygame.time.wait(2000)
        return False
    return True


class Game():
    def __init__(self):
        self.state_manager = StateManager()
        self.state_manager.screen = pygame.display.set_mode((self.state_manager.SCREEN_WIDTH,
                                                             self.state_manager.SCREEN_HEIGHT))

    def reset(self):
        self.state_manager = StateManager()

    def run(self, event):
        state_manager = self.state_manager
        jump_logic(state_manager, event)
        gravity_logic(state_manager)
        pipe_logic(state_manager)
        render(state_manager)
        return game_over_logic(state_manager)



if __name__ == "__main__":
    game = Game()
    pygame.init()
    global event
    running = True
    while running:
        event = pygame.event.poll()
        running = game.run(event)
    pygame.quit()