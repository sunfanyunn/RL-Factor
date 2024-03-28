import random
# temp
import gymnasium as gym
import numpy as np
from ple import PLE
# custom envs - don't work
# from env_design.wrapped_envs.flappy_bird_gym import PygameEnv
# from env_design.wrapped_envs.flappy_bird_gym2 import PygameEnv as PygameEnv2
# from env_design.wrapped_envs.flappy_bird_gym3 import PygameEnv as PygameEnv3

# pygame envs - do work
class PygameEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, config=None):
        super(PygameEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces object
        self.env_name = config["name"]
        from ple.games.flappybird import FlappyBird
        self.game = FlappyBird() 

        self.p = PLE(self.game, display_screen=False)
        self.p.init()
        self.all_possible_actions = self.p.getActionSet()

        # 0: do nothing; 1: flap
        self.action_space = gym.spaces.Discrete(n=len(self.all_possible_actions))  
        # self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.game.state_manager.SCREEN_WIDTH, self.game.state_manager.SCREEN_HEIGHT, 3), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape=self.get_state().shape, dtype=np.float64)

        self.current_step = 0

    def get_state(self):
        observation_dict = self.p.getGameState()
        observation = np.concatenate([np.array(observation_dict[key]).flatten() for key in sorted(observation_dict.keys())])
        return observation

    def step(self, action):
        reward = self.p.act(self.all_possible_actions[action])
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


class PygameEnv2(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, config=None):
        super(PygameEnv2, self).__init__()
        # Define action and observation space
        # They must be gym.spaces object
        self.env_name = config["name"]
        from ple.games.flappybird import FlappyBird
        self.game = FlappyBird() 

        self.p = PLE(self.game, display_screen=False)
        self.p.init()
        self.all_possible_actions = self.p.getActionSet()

        # 0: do nothing; 1: flap
        self.action_space = gym.spaces.Discrete(n=len(self.all_possible_actions))  
        # self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.game.state_manager.SCREEN_WIDTH, self.game.state_manager.SCREEN_HEIGHT, 3), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape=self.get_state().shape, dtype=np.float64)

        self.current_step = 0

    def get_state(self):
        observation_dict = self.p.getGameState()
        observation = np.concatenate([np.array(observation_dict[key]).flatten() for key in sorted(observation_dict.keys())])
        return observation

    def step(self, action):
        reward = self.p.act(self.all_possible_actions[action])
        reward = reward * 2
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


class PygameEnv3(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, config=None):
        super(PygameEnv3, self).__init__()
        # Define action and observation space
        # They must be gym.spaces object
        self.env_name = config["name"]
        from ple.games.flappybird import FlappyBird
        self.game = FlappyBird() 

        self.p = PLE(self.game, display_screen=False)
        self.p.init()
        self.all_possible_actions = self.p.getActionSet()

        # 0: do nothing; 1: flap
        self.action_space = gym.spaces.Discrete(n=len(self.all_possible_actions))  
        # self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.game.state_manager.SCREEN_WIDTH, self.game.state_manager.SCREEN_HEIGHT, 3), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape=self.get_state().shape, dtype=np.float64)

        self.current_step = 0

    def get_state(self):
        observation_dict = self.p.getGameState()
        observation = np.concatenate([np.array(observation_dict[key]).flatten() for key in sorted(observation_dict.keys())])
        return observation

    def step(self, action):
        reward = self.p.act(self.all_possible_actions[action])
        reward = reward * 10
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
    env_list = [("PygameEnv", PygameEnv), ("PygameEnv2", PygameEnv2), ("PygameEnv3", PygameEnv3)]
    selected_env_name, selected_env_class = random.choice(env_list)
    env = selected_env_class(env_config)
    env.name = selected_env_name  # Assign the environment name to a custom attribute
    return env