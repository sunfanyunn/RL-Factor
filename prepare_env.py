import gymnasium as gym
import numpy as np
import pygame
from ray.rllib.env.env_context import EnvContext
from ple import PLE

class PygameEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, config=None):
        super(PygameEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces object
        print(config)
        if config["name"] == "flappy_bird":
            from ple.games.flappybird import FlappyBird
            self.game = FlappyBird() 
        elif config["name"] == "catcher":
            from ple.games.catcher import Catcher
            self.game = Catcher() 
        elif config["name"] == "pixelcopter":
            from ple.games.pixelcopter import Pixelcopter
            self.game = Pixelcopter() 
        elif config["name"] == "puckworld": 
            from ple.games.puckworld import PuckWorld
            self.game = PuckWorld()
        elif config["name"] == "snake":
            from ple.games.snake import Snake
            self.game = Snake()
        elif config["name"] == "waterworld":
            from ple.games.waterworld import WaterWorld
            self.game = WaterWorld()
        elif config["name"] == "pong":
            from ple.games.pong import Pong
            self.game = Pong()
        else:
            assert False
        

        self.p = PLE(self.game, fps=30, display_screen=False)
        self.p.init()
        self.all_possible_actions = self.p.getActionSet()

        self.action_space = gym.spaces.Discrete(n=len(self.all_possible_actions))  # 0: do nothing; 1: flap
        #self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.game.state_manager.SCREEN_WIDTH, self.game.state_manager.SCREEN_HEIGHT, 3), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape=self.get_state().shape, dtype=np.float64)

        self.current_step = 0

    def get_state(self):
        observation_dict = self.p.getGameState()
        # sort the dictinoary and return a numpy array
        observation = np.array([observation_dict[key] for key in sorted(observation_dict.keys())])
        return observation

    def step(self, action):
        reward = self.p.act(action)
        observation = self.get_state()
        terminated = self.p.game_over()
        truncated = False
        info = {}
        # Execute one time step within the environment
        return observation, reward, terminated, truncated, info

    def reset(self, *, seed=None, options=None):
        self.p.reset_game()
        info = {}  # Additional info for debugging
        return self.get_state(), info


def env_creator(env_config):
    return PygameEnv(config=env_config) # return an env instance


if __name__ == "__main__":
    register_env("my_env", env_creator)
    env = env_creator()
    #observation, info = env.reset()
    observation, _ = env.reset()

    import imageio
    i = 0
    done = False
    total_reward = 0
    while not done:
        # action = env.action_space.sample()
        action = int(input())
        observation, reward, done, truncated, info = env.step(action)
        #imageio.imsave(f"logs/test{i}.png", observation)
        print(observation.shape, reward)
        print(reward)
        i += 1
    pygame.quit()
    env.close()