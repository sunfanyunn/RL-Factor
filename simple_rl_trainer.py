import argparse
import os
# disble tensorflow warning logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import flappy_bird_gymnasium
import gymnasium
from typing import *
import ray
from ray import air
from ray import tune
from ray.tune import registry
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.rllib.algorithms import ppo
from ray.rllib.algorithms.ppo import PPOConfig


def get_cli_args():
  parser = argparse.ArgumentParser(description="Training Script for Multi-Agent RL in Meltingpot")
  parser.add_argument(
      "--num_workers",
      type=int,
      default=0,
      help="Number of workers to use for sample collection. Setting it zero will use same worker for collection and model training.",
  )
  parser.add_argument(
      "--num_gpus",
      type=int,
      default=1,
      help="Number of GPUs to run on (can be a fraction)",
  )
  parser.add_argument(
      "--local",
      action="store_true",
      help="If enabled, init ray in local mode. Tips: use this for debugging.",
  )
  parser.add_argument(
      "--no-tune",
      action="store_true",
      help="If enabled, no hyper-parameter tuning.",
  )
  parser.add_argument(
        "--algo",
        choices=["ppo", "impala", "icm"],
        default="ppo",
        help="Algorithm to train agents.",
  )
  parser.add_argument(
        "--framework",
        choices=["tf", "torch"],
        default="torch",
        help="The DL framework specifier (tf2 eager is not supported).",
  )
  parser.add_argument(
      "--exp",
      type=str,
      default="",
      help="Name of the substrate to run",
  )
  parser.add_argument(
      "--seed",
      type=int,
      default=123,
      help="Seed to run",
  )
  parser.add_argument(
      "--results_dir",
      type=str,
      default="./results",
      help="path to save results",
  )
  parser.add_argument(
        "--logging",
        choices=["DEBUG", "INFO", "WARN", "ERROR"],
        default="INFO",
        help="The level of training and data flow messages to print.",
  )

  parser.add_argument(
        "--wandb",
        action="store_true",
        # type=bool,
        # default=False,
        help="Whether to use WanDB logging.",
  )

  parser.add_argument(
        "--downsample",
        type=bool,
        default=False,
        help="Whether to downsample substrates in MeltingPot. Defaults to 8.",
  )

  parser.add_argument(
        "--as-test",
        action="store_true",
        help="Whether this script should be run as a test.",
  )

  args = parser.parse_args()
  print("Running trails with the following arguments: ", args)
  return args


def env_creator(env_config={}):
    return gymnasium.make("FlappyBird-v0")

if __name__ == "__main__":

    args = get_cli_args()

    # Set up Ray. Use local mode for debugging. Ignore reinit error.
    # Register meltingpot environment
    ray.init(local_mode=args.local,
             _temp_dir='/ccn2/u/fanyun',
             ignore_reinit_error=True)

    registry.register_env("my_env", env_creator)
    algo = ppo.PPO(
          config={
              "env_config": {} # config to pass to the env class
          },
      ).environment(env="my_env")

    # from env_design.wrapped_envs.flappy_bird_gym import PygameEnv
    def evaluate():
        env = env_creator()
        # Get the initial observation (some value between -10.0 and 10.0).
        obs, info = env.reset()
        done = False
        total_reward = 0.0
        # Play one episode.
        while not done:
            # Compute a single action, given the current observation
            # from the environment.
            action = algo.compute_single_action(obs)
            # Apply the computed action in the environment.
            obs, reward, done, truncated, info = env.step(action)
            # Sum up rewards for reporting purposes.
            total_reward += reward
        # Report results.
        print(f"Shreaked for 1 episode; total-reward={total_reward}")

    for _ in range(100000):
        results = algo.train()
        evaluate()
