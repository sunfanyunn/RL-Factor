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


        self.p = PLE(self.game, display_screen=False)
        self.p.init()
        self.all_possible_actions = self.p.getActionSet()

        self.action_space = gym.spaces.Discrete(n=len(self.all_possible_actions))  # 0: do nothing; 1: flap
        #self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.game.state_manager.SCREEN_WIDTH, self.game.state_manager.SCREEN_HEIGHT, 3), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(-np.inf, np.inf, shape=self.get_state().shape, dtype=np.float64)

        self.current_step = 0

    def preprocess_state(self, observation_dict, padding_number=10):

        new_observation_dict = {}
        if self.game_name == "waterworld":
            for key in sorted(observation_dict.keys()):
                if key == "creep_dist":
                    continue
                if key == "creep_pos":
                    for idx in range(padding_number):
                        if len(observation_dict["creep_pos"]["GOOD"]) > idx:
                            new_observation_dict[f"good_creep_pos_{idx}"] = observation_dict["creep_pos"]["GOOD"][idx]
                        else:
                            new_observation_dict[f"good_creep_pos_{idx}"] = [0, 0]

                    for idx in range(padding_number):
                        if len(observation_dict["creep_pos"]["BAD"]) > idx:
                            new_observation_dict[f"bad_creep_pos_{idx}"] = observation_dict["creep_pos"]["BAD"][idx]
                        else:
                            new_observation_dict[f"bad_creep_pos_{idx}"] = [0, 0]
                else:
                    new_observation_dict[key] = observation_dict[key]
            return new_observation_dict

        elif self.game_name == "snake":
            for key in sorted(observation_dict.keys()):
                if key == "snake_body":
                    continue
                if key == 'snake_body_pos':
                    for idx in range(padding_number):
                        if len(observation_dict["snake_body_pos"]) > idx:
                            new_observation_dict[f"snake_body_pos_{idx}"] = observation_dict["snake_body_pos"][idx]
                        else:
                            new_observation_dict[f"snake_body_pos_{idx}"] = [0, 0]
                else:
                    new_observation_dict[key] = observation_dict[key]
            return new_observation_dict

        else:
            return observation_dict

    def get_state(self):
        observation_dict = self.p.getGameState()
        observation_dict = self.preprocess_state(observation_dict)
        observation = np.concatenate([np.array(observation_dict[key]).flatten() for key in sorted(observation_dict.keys())])
        return observation

    def step(self, action):
        reward = self.p.act(self.all_possible_actions[action])
        observation = self.get_state()
        terminated = self.p.game_over()
        truncated = False
        info = {}
        # Execute one time step within the environment

        ### game specific logics
        if self.game_name == "snake":
            observation_dict = self.p.getGameState()
            if len(observation_dict["snake_body_pos"]) >= 10:
                terminated = True
        if self.game_name == "waterworld":
            observation_dict = self.p.getGameState()
            if len(observation_dict["creep_pos"]["BAD"]) > 10:
                terminated = True

        return observation, reward, terminated, truncated, info

    def reset(self, *, seed=None, options=None):
        self.p.reset_game()
        info = {}  # Additional info for debugging
        return self.get_state(), info


def env_creator(env_config):
    return PygameEnv(config=env_config) # return an env instance


if __name__ == "__main__":
    from ray.rllib.utils import check_env
    for env_name in ["waterworld", "snake"]:
        env_config = {"name": env_name}
        env = env_creator(env_config)
        print(env.p.getActionSet())
        check_env(env)
        print(f"{env_name} passed")

        #observation, info = env.reset()
        observation, info = env.reset()
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