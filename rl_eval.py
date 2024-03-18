import numpy as np
import ray
from ray.rllib.algorithms import ppo, dqn, impala
from ray.tune import registry
#from ray.tune import checkpoint_manager as cm


def eval_one_episode(trainer, env):
    # Evaluate the policy
    obs, _ = env.reset()
    done = False
    total_reward = 0
    while not done:
        action = trainer.compute_single_action(obs)
        obs, reward, done, truncated, info = env.step(action)
        total_reward += reward
        # env.render()  # This depends on the environment having a render method
    return total_reward


def evaluate(env_creator, best_checkpoint_path, NUM_TRIALS=10):
    # Initialize Ray
    ray.init(ignore_reinit_error=True)
    # Register environment
    registry.register_env("my_env", env_creator)
    env = env_creator()

    trainer = ppo.PPO(env="my_env")
    # Load the best checkpoint
    trainer.restore(best_checkpoint_path)

    total_rewards = []
    for _ in range(NUM_TRIALS):
        total_reward = eval_one_episode(trainer, env)
        total_rewards.append(total_reward)

    env.close()
    ray.shutdown()
    return np.mean(total_rewards), np.std(total_rewards)


if __name__ == '__main__':
    from run_env_generation import env_creator
    #best_checkpoint_path = "/data2/sunfanyun/LLM-Curriculum/results/torch/simple_flappy_bird_ppo/PPO_my_env_ae957_00000_0_2024-02-16_11-22-11/checkpoint_000866"
    best_checkpoint_path = "results/torch-ppo/factor-baselines/PPO_my_env_5c853_00000_0_entropy_coeff=0.1715,gamma=0.9735,lr=0.0004_2024-02-23_02-07-33/checkpoint_000199"
    print(evaluate(env_creator, best_checkpoint_path))
