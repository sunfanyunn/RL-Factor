import pygame
import sys
import random


class StateManager:
    def __init__(self):
        # Initialize state variables directly
        self.board = [[" "] * 3 for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None

        self.screen = pygame.display.set_mode((300, 300))
        self.clock = pygame.time.Clock()


def reset_game(state_manager):
    # Reset the game state
    state_manager.board = [[" "] * 3 for _ in range(3)]
    state_manager.current_player = "X"
    state_manager.game_over = False
    state_manager.winner = None


def render(state_manager):
    state_manager.screen.fill((255, 255, 255))  # Fill the screen with white

    # Render the Tic-Tac-Toe board
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(
                state_manager.screen, (0, 0, 0), (col * 100, row * 100, 100, 100), 2
            )
            font = pygame.font.Font(None, 36)
            text = font.render(state_manager.board[row][col], True, (0, 0, 0))
            state_manager.screen.blit(text, (col * 100 + 40, row * 100 + 40))

    if state_manager.winner:
        font = pygame.font.Font(None, 36)
        winner_text = font.render(f"Winner: {state_manager.winner}", True, (0, 0, 0))
        state_manager.screen.blit(winner_text, (10, 10))

    pygame.display.flip()
    state_manager.clock.tick(60)


def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None


def perform_action(state_manager, action):
    # Apply the action to the Tic-Tac-Toe board
    row, col = action
    if state_manager.board[row][col] == " ":
        state_manager.board[row][col] = state_manager.current_player
        state_manager.current_player = (
            "X" if state_manager.current_player == "O" else "O"
        )
    else:
        # Invalid move, penalize the agent with a negative reward
        return -1

    # Check for a winner or a draw
    winner = check_winner(state_manager.board)
    if winner:
        state_manager.game_over = True
        state_manager.winner = winner
        return 1  # Positive reward for winning
    elif all(state != " " for row in state_manager.board for state in row):
        state_manager.game_over = True
        return 0  # Zero reward for a draw

    return 0  # No immediate reward if the game is still ongoing


def main():
    pygame.init()
    state_manager = StateManager()

    running = True
    while running:
        action = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not state_manager.game_over:
                # Translate mouse click to Tic-Tac-Toe board coordinates
                action = (event.pos[1] // 100, event.pos[0] // 100)

        if not state_manager.game_over and action:
            reward = perform_action(state_manager, action)

        render(state_manager)

        # Check for game over and restart
        if state_manager.game_over:
            pygame.time.delay(2000)  # Delay for 2 seconds before restarting
            reset_game(state_manager)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tic-Tac-Toe")
    main()
