import gymnasium as gym
import numpy as np
import pygame
from env_design.envs.flappy_bird_test import Game


class PygameEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, config=None):
        super(PygameEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        pygame.init()
        self.game = Game()  # Initialize your game class

        self.action_space = gym.spaces.Discrete(n=2)  # 0: do nothing; 1: flap
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.game.state_manager.SCREEN_WIDTH, self.game.state_manager.SCREEN_HEIGHT, 3), dtype=np.uint8)

        self.done = False
        self.previous_score = 0
        self.current_step = 0

    def get_reward(self):
        current_score = self.game.state_manager.score
        if current_score > self.previous_score:
            self.previous_score = current_score 
            return 1
        return 0

    def perform_action(self, action):
        # Implement action handling here
        if action == 1:
            return pygame.event.Event(pygame.MOUSEBUTTONDOWN)
        else:
            return pygame.event.Event(pygame.NOEVENT)
        
    def step(self, action):
        # Execute one time step within the environment
        event = self.perform_action(action)
        running = self.game.run(event)
        for _ in range(5):
            event = pygame.event.poll()
            running = self.game.run(event)
            if not running:
                break

        observation = pygame.surfarray.array3d(self.game.state_manager.screen)
        reward = self.get_reward()
        terminated = not running 
        truncated = False
        info = {}  # Additional info for debugging
        return observation, reward, terminated, info
    
    def reset(self, *, seed=None, options=None):
        self.game.reset()
        running = self.game.run(pygame.event.Event(pygame.NOEVENT))
        pygame.display.flip()
        observation = pygame.surfarray.array3d(self.game.state_manager.screen)
        info = {}  # Additional info for debugging
        return observation


if __name__ == "__main__":
    env = PygameEnv()
    observation = env.reset()
    print(observation.shape, observation.dtype)

    done = False
    while not done:
        action = int(input())
        observation, reward, done, info = env.step(action)
        print(observation.shape)
    pygame.quit()
    env.close()
