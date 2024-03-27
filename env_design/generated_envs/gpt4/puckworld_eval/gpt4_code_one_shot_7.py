import pygame
import sys
import random
import math

WIDTH, HEIGHT = 640, 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

GREEN_REWARD = 100
RED_PENALTY_FACTOR = 2


class Game:

    def __init__(self):
        """Initialize the game
        agent: the player's character
        green_dot: the target for the agent
        red_puck: the obstacle for the agent
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PuckWorld")
        self.clock = pygame.time.Clock()
        self.agent = Agent()
        self.green_dot = GreenDot()
        self.green_dot.randomize_position()
        self.red_puck = RedPuck()
        self.score = 0
        self.running = True

    def run(self, event):
        """The game loop."""
        while self.running:
            self.screen.fill(BLACK)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.agent.apply_thrusters(keys)

            self.agent.update()
            self.red_puck.update(self.agent)
            self.green_dot.update()

            # Update the score
            self.score += self.calculate_score()

            # Draw all sprites
            self.screen.blit(self.agent.image, self.agent.rect)
            self.screen.blit(self.green_dot.image, self.green_dot.rect)
            self.screen.blit(self.red_puck.image, self.red_puck.rect)

            # Draw the score
            score_text = pygame.font.SysFont(None, 36).render('Score: ' + str(int(self.score)), True, WHITE)
            self.screen.blit(score_text, (10, 10))

            # Update the display
            pygame.display.flip()

            self.clock.tick(FPS)

        return False

    def calculate_score(self):
        """Calculate score based on proximity."""
        distance_to_green = self.get_distance(self.agent.rect, self.green_dot.rect)
        distance_to_red = self.get_distance(self.agent.rect, self.red_puck.rect)

        if distance_to_green < self.green_dot.image.get_width() / 2:
           self.green_dot.randomize_position()
           return GREEN_REWARD
        else:
           score = max(GREEN_REWARD - distance_to_green, 0)
           score -= RED_PENALTY_FACTOR * max(0, self.red_puck.image.get_width() / 2 - distance_to_red)
           return score / 10

    def get_distance(self, rect1, rect2):
        """Calculate distance between two points."""
        return math.hypot(rect1.centerx - rect2.centerx, rect1.centery - rect2.centery)


# Definitions for Agent, RedPuck, and GreenDot classes with necessary method implementations
# ... (omitted for brevity)

if __name__ == "__main__":
    game = Game()
    game.run(None)
    pygame.quit()
    sys.exit()
