import gym
from gym.spaces import Discrete, Box
import numpy as np
import pygame
from env_design.envs.flappy_bird_test import Game

class PygameEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self):
        super(PygameEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = Discrete(n=2)  # 0: do nothing; 1: flap
        self.screen_height = 800
        self.screen_width = 600
        self.observation_space = Box(low=0, high=255, shape=(self.screen_height, self.screen_width, 3), dtype=np.uint8)

        self.game = Game()  # Initialize your game class
        pygame.init()
        global event
        self.done = False
        self.previous_score = 0

    def get_reward(self):
        current_score = self.game.state_manager.score
        if current_score > self.previous_score:
            self.previous_score = current_score
            return 1
        return 0

    def perform_action(self, action):
        # Implement action handling here
        if action == 1:
            # Trigger the flap action
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        
    def step(self, action):
        # Execute one time step within the environment
        self.perform_action(action)
        event = pygame.event.poll()
        running = self.game.run(event)
        pygame.display.flip()
        observation = pygame.surfarray.array3d(self.game.state_manager.screen)
        reward = self.get_reward()
        done = not running 
        info = {}  # Additional info for debugging
        return observation, reward, done, info
    
    def reset(self):
        event = pygame.event.poll()
        running = self.game.run(event)
        pygame.display.flip()
        observation = pygame.surfarray.array3d(self.game.state_manager.screen)
        reward = self.game.state_manager.score
        done = not running 
        info = {}  # Additional info for debugging
        return observation, reward, done, info


if __name__ == "__main__":
    env = PygameEnv()
    observation = env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print(reward)
    pygame.quit()
    env.close()
