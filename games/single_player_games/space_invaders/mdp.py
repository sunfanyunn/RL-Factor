import pygame
import sys


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.screen_width = 800
        self.screen_height = 600
        self.player_position = {"x": 400, "y": 550}
        self.player_speed = 20
        self.alien_positions = []
        self.bullet_position = {"x": 0, "y": 0}
        self.bullet_speed = 15
        self.score = 0
        self.game_over = False

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()


def render(state_manager):
    state_manager.screen.fill((0, 0, 0))  # Fill the screen with black

    pygame.draw.rect(
        state_manager.screen,
        (255, 255, 255),
        (
            state_manager.player_position["x"],
            state_manager.player_position["y"],
            50,
            20,
        ),
    )

    # Render aliens
    for alien in state_manager.alien_positions:
        pygame.draw.rect(
            state_manager.screen,
            (0, 255, 0),
            (
                alien["x"],
                alien["y"],
                30,
                30,
            ),
        )

    # Render bullet
    if state_manager.bullet_position["y"] > 0:
        pygame.draw.rect(
            state_manager.screen,
            (0, 255, 255),
            (
                state_manager.bullet_position["x"],
                state_manager.bullet_position["y"],
                5,
                10,
            ),
        )

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {state_manager.score}", True, (255, 255, 255))
    state_manager.screen.blit(score_text, (10, 10))

    pygame.display.flip()
    state_manager.clock.tick(60)


def player_movement(state_manager, direction):
    if direction == "LEFT":
        state_manager.player_position["x"] -= state_manager.player_speed
    elif direction == "RIGHT":
        state_manager.player_position["x"] += state_manager.player_speed

    # Ensure the player stays within the screen boundaries
    state_manager.player_position["x"] = max(
        0,
        min(
            state_manager.screen_width - 50,
            state_manager.player_position["x"],
        ),
    )


def spawn_aliens(state_manager):
    if len(state_manager.alien_positions) == 0:
        for i in range(5):
            for j in range(5):
                new_alien = {
                    "x": 50 + i * 100,
                    "y": 50 + j * 50,
                    "direction": 1,  # 1 for right, -1 for left
                }
                state_manager.alien_positions.append(new_alien)

    # Determine if the entire group needs to change direction and descend
    change_direction = False
    for alien in state_manager.alien_positions:
        if alien["x"] <= 0 or alien["x"] >= state_manager.screen_width - 30:
            change_direction = True
            break

    if change_direction:
        for alien in state_manager.alien_positions:
            alien["direction"] *= -1
            alien["y"] += 20

    for alien in state_manager.alien_positions:
        alien["x"] += 0.5 * alien["direction"]  # Move side by side
        # alien["y"] += 0.5  # Descend slowly

    if all(
        alien["y"] > state_manager.screen_height
        for alien in state_manager.alien_positions
    ):
        # Create a new group of aliens
        state_manager.alien_positions = []
        for i in range(5):
            for j in range(5):
                new_alien = {
                    "x": 50 + i * 100,
                    "y": 50 + j * 50,
                    "direction": 1,
                }
                state_manager.alien_positions.append(new_alien)


def bullet_movement(state_manager):
    if state_manager.bullet_position["y"] > 0:
        state_manager.bullet_position["y"] -= state_manager.bullet_speed
    else:
        state_manager.bullet_position["y"] = 0

    for alien in state_manager.alien_positions:
        if (
            alien["x"] < state_manager.bullet_position["x"] < alien["x"] + 30
            and alien["y"] < state_manager.bullet_position["y"] < alien["y"] + 30
        ):
            state_manager.alien_positions.remove(alien)
            state_manager.bullet_position["y"] = 0
            state_manager.score += 1


def check_game_over(state_manager):
    if not state_manager.alien_positions:
        return

    if state_manager.alien_positions[0]["y"] >= state_manager.screen_height:
        state_manager.game_over = True

    if state_manager.game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_movement(state_manager, "LEFT")
                elif event.key == pygame.K_RIGHT:
                    player_movement(state_manager, "RIGHT")
                elif (
                    event.key == pygame.K_SPACE
                    and state_manager.bullet_position["y"] == 0
                ):
                    state_manager.bullet_position["x"] = (
                        state_manager.player_position["x"] + 25
                    )
                    state_manager.bullet_position["y"] = state_manager.player_position[
                        "y"
                    ]

        spawn_aliens(state_manager)

        bullet_movement(state_manager)

        check_game_over(state_manager)

        render(state_manager)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Moving Shooting Space Invaders")
    main()
