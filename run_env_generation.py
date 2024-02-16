import pickle
import importlib
import json
import argparse
import os
import sys
from game_structure import GameRep
from openai import OpenAI


# from env_design.wrapped_envs.flappy_bird_gym import PygameEnv
# def env_creator(env_config={}):
#     return PygameEnv()  # return an env instance
import gymnasium
import flappy_bird_gymnasium
def env_creator(env_config={}):
    return gymnasium.make("FlappyBird-v0")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Game Parameters')
    parser.add_argument('--log_dir', type=str, help='Directory for logs')
    parser.add_argument('--env_name', type=str, help='Environment name')
    parser.add_argument('--game_template', type=str, help='Game template')
    parser.add_argument('--debug_mode', type=int, default=3, choices=[1, 2, 3], help='Debug mode')

    # Parse arguments
    args = parser.parse_args()

    if False:
        # Use arguments
        log_dir = args.log_dir
        game_template = args.game_template
        debug_mode = args.debug_mode

        client = OpenAI()

        game = GameRep(log_dir=args.log_dir, debug_mode=debug_mode, client=client)
        pass_test, error_msg = game.pass_sanity_check()
        print(error_msg)
        assert pass_test

        # load game rep from a file and evaluate
        filename = sys.argv[2]
        game = pickle.load(open(filename, "rb"))
        game.client = client
        code = game.export_code()
        implementation_path = "env_design/envs/flappy_bird_test.py"
        with open(implementation_path, "w") as f:
            f.write(code)

    register_env("my_env", env_creator)
