import argparse
import os
# disble tensorflow warning logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from typing import *

import ray
from ray import air
from ray import tune
from ray.tune import registry
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.rllib.core.rl_module.rl_module import SingleAgentRLModuleSpec
from randomize_env_test import env_creator


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
          choices=["dreamerv3", "ppo", "dqn", "impala", "icm"],
          default="ppo",
          help="Algorithm to train agents.",
    )
    parser.add_argument(
          "--framework",
          choices=["tf2", "torch"],
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
          # default=False,
          help="Whether to use WanDB logging.",
    )
    parser.add_argument(
          "--factor",
          action="store_true",
          default=False,
          help="Whether to use factor GNN.",
    )
    parser.add_argument(
          "--env_name",
          default="default",
          help="",
    )
    parser.add_argument(
          "--env_id",
          default="default",
          help="",
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


# class CustomWandbLoggerCallback(WandbLoggerCallback):
#     def on_train_result(self, *, algorithm, result, **kwargs):
#         result["env_name"] = result["custom_metrics"]["env_name"]
#         super().on_train_result(algorithm=algorithm, result=result, **kwargs)

class CustomWandbLoggerCallback(WandbLoggerCallback):
    def on_episode_end(self, *, worker, base_env, policies, episode, env_index, **kwargs):
        env_name = base_env.get_unwrapped()[0].env_name
        wandb.config.update({"env_name": env_name}, allow_val_change=True)
        super().on_episode_end(worker=worker, base_env=base_env, policies=policies,
                               episode=episode, env_index=env_index, **kwargs)


if __name__ == "__main__":

    args = get_cli_args()
    # Set up Ray. Use local mode for debugging. Ignore reinit error.
    # Register environment
    #registry.register_env("my_env", env_creator)
    registry.register_env("my_env", lambda config: env_creator(config))

    # initialize default configurations for native RLlib algorithms (we use one solver 
    # all exploration modules)  
    # Fetch experiment configurations
    #from configs import get_experiment_config
    # hyperparameter search
    from meta_rl_configs import get_experiment_config
    if args.algo == "dreamerv3":
        assert False
        from ray.rllib.algorithms import dreamerv3
        trainer = "DreamerV3"
        num_gpus = args.num_gpus
        default_config = dreamerv3.DreamerV3Config()
        configs, exp_config, tune_config = get_experiment_config(args, default_config)

    if args.algo == "ppo":
        trainer = "PPO"
        from ray.rllib.algorithms import ppo
        default_config = ppo.PPOConfig()
        configs, exp_config, tune_config = get_experiment_config(args, default_config)

    elif args.algo == 'dqn':
        trainer = "DQN"
        from ray.rllib.algorithms import dqn
        default_config = dqn.DQNConfig()
        configs, exp_config, tune_config = get_experiment_config(args, default_config)


    elif args.algo == "impala":
        trainer = "IMPALA"
        from ray.rllib.algorithms import impala
        default_config = impala.ImpalaConfig()
        configs, exp_config, tune_config = get_experiment_config(args, default_config)

    elif args.algo == "icm":
       assert False

    else:
        print('The selected option is not tested. You may encounter issues if you use the baseline \
              policy configurations with non-tested algorithms')

    # Ensure GPU is available if set to True
    if configs.num_gpus > 0 and args.framework == "torch":
       import torch
       if torch.cuda.is_available():
          print("Using GPU device.")
       else:
          print("Either GPU is not available on this machine or not visible to this run. Training using CPU only.")
          configs.num_gpus = 0

    # Setup WanDB    
    if "WANDB_API_KEY" in os.environ and args.wandb:
      wandb_project = f'{args.exp}_{args.framework}'
      wandb_group = f'{args.env_id}-{args.env_name}-{args.algo}'

      # Set up Weights And Biases logging if API key is set in environment variable.
      wdb_callbacks = [
            CustomWandbLoggerCallback(
                project=wandb_project,
                group=wandb_group,
                api_key=os.environ["WANDB_API_KEY"],
                log_config=True,
          )
      ]
    else:
      wdb_callbacks = []
      print("WARNING! No wandb API key found, running without wandb!")

    ### I changed the _temp_dir but you likely don't have to do so
    # _temp_dir='/data2/sunfanyun/tmp',
    ray.init(local_mode=args.local, ignore_reinit_error=True)
    ### for some reason, I have to set the following line, otherwiseI will get "URI has empty scheme"
    # exp_config['dir'] = None

    # Setup hyper-parameter optimization configs here
    # hyperparam tuning - documentation for tune.TuneConfig: https://docs.ray.io/en/latest/tune/api/doc/ray.tune.TuneConfig.html#ray.tune.TuneConfig
    if not args.no_tune:
     # NotImplementedError
     tune_config = None
    else:
     tune_config = tune.TuneConfig(reuse_actors=False)

    # Setup checkpointing configurations documentation
    # https://docs.ray.io/en/latest/train/api/doc/ray.train.CheckpointConfig.html?highlight=checkpoint_score_attribute
    ckpt_config = air.CheckpointConfig(
      num_to_keep=exp_config['keep'],
      checkpoint_score_attribute=exp_config['checkpoint_score_attr'],
      checkpoint_score_order=exp_config['checkpoint_score_order'],
      checkpoint_frequency=exp_config['freq'],
      checkpoint_at_end=exp_config['end'])

    # documentation for air.RunConfig https://github.com/ray-project/ray/blob/c3a9756bf0c7691679edb679f666ae39614ba7e8/python/ray/air/config.py#L575
    run_config=air.RunConfig(
      name=exp_config['name'],
      callbacks=wdb_callbacks,
      storage_path=exp_config['dir'],
      local_dir=exp_config['dir'],
      stop=exp_config['stop'],
      checkpoint_config=ckpt_config,
      verbose=3)

    # Run Trials documentation https://docs.ray.io/en/latest/tune/api/doc/ray.tune.Tuner.html#ray-tune-tuner  
    results = tune.Tuner(
        trainer, # trainable to be tuned
        param_space=configs.to_dict(),
        tune_config=tune_config,
        run_config=run_config,
    ).fit()

    best_result = results.get_best_result(metric="episode_reward_mean", mode="max")
    print(best_result)

#  best_checkpoint_path = best_result.checkpoint.path
#  from rl_eval import eval
#  print('======================= Final Result ===============================')
#  print(eval(env_creator, best_checkpoint_path, NUM_TRIALS=100))
