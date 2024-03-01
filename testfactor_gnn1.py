"""
Example of define custom tokenizers for recurrent models in RLModules.

This example shows the following steps:
- Define a custom tokenizer for a recurrent encoder.
- Define a model config that builds the custom tokenizer.
- Modify the default PPOCatalog to use the custom tokenizer config.
- Run a training that uses the custom tokenizer.
"""

import argparse
import os

import ray
from ray import air, tune
from ray.tune.registry import register_env
from ray.rllib.examples.env.repeat_after_me_env import RepeatAfterMeEnv
from ray.rllib.examples.env.repeat_initial_obs_env import RepeatInitialObsEnv
from ray.rllib.core.rl_module.rl_module import SingleAgentRLModuleSpec
from ray.rllib.policy.sample_batch import SampleBatch
from dataclasses import dataclass
from ray.rllib.core.models.specs.specs_dict import SpecDict
from ray.rllib.core.models.specs.specs_base import TensorSpec
from ray.rllib.core.models.base import Encoder, ENCODER_OUT
from ray.rllib.core.models.torch.base import TorchModel
from ray.rllib.core.models.tf.base import TfModel
from ray.rllib.algorithms.ppo.ppo import PPOConfig
from ray.rllib.algorithms.ppo.ppo_catalog import PPOCatalog
from ray.rllib.utils.framework import try_import_tf, try_import_torch
from ray.rllib.utils.test_utils import check_learning_achieved
from ray.rllib.core.models.configs import ModelConfig

from ray.rllib.algorithms.ppo.torch.ppo_torch_rl_module import PPOTorchRLModule
from ray.rllib.core.rl_module.rl_module import RLModuleConfig
from ray.rllib.utils.nested_dict import NestedDict
from ray.rllib.core.rl_module.torch.torch_rl_module import TorchRLModule

from ray.rllib.core.rl_module.torch.torch_rl_module import TorchRLModule
from ray.rllib.core.rl_module.rl_module import RLModuleConfig
from ray.rllib.utils.nested_dict import NestedDict

import torch
import torch.nn as nn
from typing import Mapping, Any

from factor_gnn import FactorGraph


parser = argparse.ArgumentParser()

tf1, tf, tfv = try_import_tf()
torch, nn = try_import_torch()

parser.add_argument("--env", type=str, default="RepeatAfterMeEnv")
parser.add_argument("--num-cpus", type=int, default=0)
parser.add_argument(
    "--framework",
    choices=["tf", "tf2", "torch"],
    default="torch",
    help="The DL framework specifier.",
)
parser.add_argument(
    "--as-test",
    action="store_true",
    help="Whether this script should be run as a test: --stop-reward must "
    "be achieved within --stop-timesteps AND --stop-iters.",
)
"""parser.add_argument(
    "--stop-iters", type=int, default=100, help="Number of iterations to train."
)
parser.add_argument(
    "--stop-timesteps", type=int, default=100000, help="Number of timesteps to train."
)
parser.add_argument(
    "--stop-reward", type=float, default=90.0, help="Reward at which we stop training."
)"""
parser.add_argument(
    "--stop-iters", type=int, default=1, help="Number of iterations to train."
)
parser.add_argument(
    "--stop-timesteps", type=int, default=1, help="Number of timesteps to train."
)
parser.add_argument(
    "--stop-reward", type=float, default=10.0, help="Reward at which we stop training."
)
parser.add_argument(
    "--local-mode",
    action="store_true",
    help="Init Ray in local mode for easier debugging.",
)

# We first define a custom tokenizer that we want to use to encode the
# observations before they are passed into the recurrent cells.
# We do this step for tf and for torch here to make the following steps framework-
# agnostic. However, if you use only one framework, you can skip the other one.

from factor_gnn import FactorGraph

#class FactorGraphRL_(PPOTorchRLModule):
class FactorGraphRL(TorchRLModule):
    def __init__(self, config: RLModuleConfig) -> None:
        super().__init__(config)

    def setup(self):
        # access the factors
        factors = self.config.model_config_dict["factors"]
        print(factors)
        self.policy = FactorGraph(factors)

    def _forward_inference(self, batch: NestedDict) -> Mapping[str, Any]:
        with torch.no_grad():
            return self._forward_train(batch)

    def _forward_exploration(self, batch: NestedDict) -> Mapping[str, Any]:
        with torch.no_grad():
            return self._forward_train(batch)

    def _forward_train(self, batch: NestedDict) -> Mapping[str, Any]:
        # 32, 2
        print(batch["obs"].shape)
        import pdb;pdb.set_trace()
        action_logits = self.policy(batch["obs"])
        return {"action_dist": torch.distributions.Categorical(logits=action_logits)}


if __name__ == "__main__":
    args = parser.parse_args()
    factors = [
        {
            "factor_name": "jump_logic",
            "used_state_variables": [
                {"name": "game_over", "type": "bool", "dimensionality": "scalar"},
                {"name": "jump_velocity", "type": "int", "dimensionality": "scalar"}
            ],
            "modified_state_variables": [
                {"name": "bird_position_y", "type": "int", "dimensionality": "scalar"}
            ]
        },
        {
            "factor_name": "gravity_logic",
            "used_state_variables": [
                {"name": "gravity", "type": "int", "dimensionality": "scalar"}
            ],
            "modified_state_variables": [
                {"name": "bird_position_y", "type": "int", "dimensionality": "scalar"}
            ]
        },
        {
            "factor_name": "pipe_logic",
            "used_state_variables": [
                {"name": "bird_position_x", "type": "int", "dimensionality": "scalar"},
                {"name": "bird_position_y", "type": "int", "dimensionality": "scalar"},
                {"name": "bird_size", "type": "int", "dimensionality": "scalar"},
                {"name": "SCREEN_WIDTH", "type": "int", "dimensionality": "scalar"},
                {"name": "PIPE_WIDTH", "type": "int", "dimensionality": "scalar"},
                {"name": "PIPE_GAP", "type": "int", "dimensionality": "scalar"},
                {"name": "pipe_positions", "type": "list", "dimensionality": "collection"}
            ],
            "modified_state_variables": [
                {"name": "pipe_positions", "type": "list", "dimensionality": "collection"},
                {"name": "score", "type": "int", "dimensionality": "scalar"},
                {"name": "game_over", "type": "bool", "dimensionality": "scalar"}
            ]
        },
        {
            "factor_name": "game_over_logic",
            "used_state_variables": [
                {"name": "bird_position_y", "type": "int", "dimensionality": "scalar"},
                {"name": "SCREEN_HEIGHT", "type": "int", "dimensionality": "scalar"}
            ],
            "modified_state_variables": [
                {"name": "game_over", "type": "bool", "dimensionality": "scalar"}
            ]
        }
    ]

    ray.init(num_cpus=args.num_cpus or None, local_mode=args.local_mode) 
    register_env("RepeatAfterMeEnv", lambda c: RepeatAfterMeEnv(c))
    register_env("RepeatInitialObsEnv", lambda _: RepeatInitialObsEnv())

    config = (
        PPOConfig()
        .experimental(_enable_new_api_stack=True)
        .environment(args.env, env_config={"repeat_delay": 2})
        .framework(args.framework)
        .rollouts(num_rollout_workers=0, num_envs_per_worker=20)
        .training(
            #model={
            #    "use_lstm": False,
            #    "fcnet_hiddens": [256],
            #},
            gamma=0.9,
            entropy_coeff=0.001,
            vf_loss_coeff=1e-5,
        )
        .rl_module(
            rl_module_spec=SingleAgentRLModuleSpec(module_class=FactorGraphRL,
                                                   model_config_dict={"factors": factors})
                                                   #catalog_class=CustomPPOCatalog)
        )
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        .resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0")))
    )

    stop = {
        "training_iteration": args.stop_iters,
        "timesteps_total": args.stop_timesteps,
        "episode_reward_mean": args.stop_reward,
    }

    tuner = tune.Tuner(
        "PPO",
        param_space=config.to_dict(),
        run_config=air.RunConfig(stop=stop, verbose=1),
    )
    results = tuner.fit()

    if args.as_test:
        check_learning_achieved(results, args.stop_reward)
    ray.shutdown()