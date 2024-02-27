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
        self.game_name = config["name"]
        if self.game_name == "flappy_bird":
            from ple.games.flappybird import FlappyBird
            self.game = FlappyBird() 
        elif self.game_name == "catcher":
            from ple.games.catcher import Catcher
            self.game = Catcher() 
        elif self.game_name == "pixelcopter":
            from ple.games.pixelcopter import Pixelcopter
            self.game = Pixelcopter() 
        elif self.game_name == "puckworld": 
            from ple.games.puckworld import PuckWorld
            self.game = PuckWorld()
        elif self.game_name == "snake":
            from ple.games.snake import Snake
            self.game = Snake()
        elif self.game_name == "waterworld":
            from ple.games.waterworld import WaterWorld
            self.game = WaterWorld()
        elif self.game_name == "pong":
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
        if self.game_name == "waterworld":
            observations = []
            for key in sorted(observation_dict.keys()):
                if key == 'creep_pos':
                    observations.append( \
                        np.concatenate([np.array(observation_dict['creep_pos'][k]).flatten() for k in sorted(observation_dict['creep_pos'].keys())])
                    )
                else:
                    observations.append(np.array(observation_dict[key]).flatten())
            observation = np.concatenate(observations)
        elif self.game_name == "snake":
            observations = []
            for key in sorted(observation_dict.keys()):
                if key == 'snake_body_pos':
                    body_pos = np.array(observation_dict['snake_body_pos'])
                    observations.append(body_pos[:5].flatten())
                else:
                    observations.append(np.array(observation_dict[key]).flatten())
            observation = np.concatenate([np.array(observation_dict[key]).flatten() for key in sorted(observation_dict.keys())])
        else:
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


def env_creator(env_config):
    return PygameEnv(config=env_config) # return an env instance


if __name__ == "__main__":
    from ray.rllib.utils import check_env
    for env_name in ["pong", "snake", "waterworld"]:
        env_config = {"name": env_name}
        env = env_creator(env_config)
        print(env.p.getActionSet())
        check_env(env)
        print(f"{env_name} passed")
        input()

    #observation, info = env.reset()
    observation, info = env.reset()
    import pdb;pdb.set_trace()
    print(observation.shape)
    print(env.p.getGameState())

    done = False
    for _ in range(10):
        i = 0
        total_reward = 0
        while not done:
            action = env.action_space.sample()
            observation, reward, done, truncated, info = env.step(action)
            total_reward += reward
            i += 1
        print(total_reward)
    env.close()
