import pickle
import importlib
import json
import argparse
import os
import sys
from game_structure import GameRep
from openai import OpenAI
from ray.rllib.algorithms.ppo import PPOConfig


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

        #api_key_path = '/ccn2/u/locross/llmv_marl/llm_plan/lc_api_key.json'
        api_key_path = '/Users/locro/Documents/Stanford/lc_api_key.json'
        OPENAI_KEYS = json.load(open(api_key_path, 'r'))
        api_key = OPENAI_KEYS['API_KEY']
        client = OpenAI(api_key=api_key)

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

    from env_design.wrapped_envs.flappy_bird_gym import PygameEnv
    # Create an RLlib Algorithm instance from a PPOConfig to learn how to
    # act in the above environment.
    config = (
        PPOConfig()
        .environment(
            # Env class to use (here: our gym.Env sub-class from above).
            env=PygameEnv,
            # Config dict to be passed to our custom env's constructor.
            env_config={
            },
        )
        # Parallelize environment rollouts.
        .rollouts(num_rollout_workers=3)
    )
    # Use the config's `build()` method to construct a PPO object.
    algo = config.build()

    # Train for n iterations and report results (mean episode rewards).
    for iteration in range(100000):
        results = algo.train()
        print(f"Iter: {i}; avg. reward={results['episode_reward_mean']}")

        if iteration % 100 == 0:
            env = PygameEnv()
            # Get the initial observation (some value between -10.0 and 10.0).
            obs, info = env.reset()
            terminated = truncated = False
            total_reward = 0.0
            # Play one episode.
            while not terminated and not truncated:
                # Compute a single action, given the current observation
                # from the environment.
                action = algo.compute_single_action(obs)
                # Apply the computed action in the environment.
                obs, reward, terminated, truncated, info = env.step(action)
                # Sum up rewards for reporting purposes.
                total_reward += reward
            # Report results.
            print(f"Shreaked for 1 episode; total-reward={total_reward}")
