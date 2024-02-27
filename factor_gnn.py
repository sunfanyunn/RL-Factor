import torch
import torch.nn as nn
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2

import numpy as np
import logging
import gymnasium as gym

from ray.rllib.models.modelv2 import ModelV2, restore_original_dimensions
from ray.rllib.models.torch.torch_action_dist import TorchCategorical
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
#from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC
from ray.rllib.utils.annotations import override
from ray.rllib.utils.framework import try_import_torch
from ray.rllib.offline import JsonReader


torch, nn = try_import_torch()


from ray.rllib.models.torch.misc import SlimFC, AppendBiasLayer, normc_initializer
from ray.rllib.utils.typing import Dict, TensorType, List, ModelConfigDict

torch, nn = try_import_torch()

logger = logging.getLogger(__name__)


class FullyConnectedNetwork(TorchModelV2, nn.Module):
    """Generic fully connected network."""

    def __init__(
        self,
        obs_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        num_outputs: int,
        model_config: ModelConfigDict,
        name: str,
    ):
        TorchModelV2.__init__(
            self, obs_space, action_space, num_outputs, model_config, name
        )
        nn.Module.__init__(self)

        hiddens = list(model_config.get("fcnet_hiddens", [])) + list(
            model_config.get("post_fcnet_hiddens", [])
        )
        activation = model_config.get("fcnet_activation")
        if not model_config.get("fcnet_hiddens", []):
            activation = model_config.get("post_fcnet_activation")
        no_final_linear = model_config.get("no_final_linear")
        self.vf_share_layers = model_config.get("vf_share_layers")
        self.free_log_std = model_config.get("free_log_std")
        # Generate free-floating bias variables for the second half of
        # the outputs.
        if self.free_log_std:
            assert num_outputs % 2 == 0, (
                "num_outputs must be divisible by two",
                num_outputs,
            )
            num_outputs = num_outputs // 2

        layers = []
        prev_layer_size = int(np.product(obs_space.shape))
        self._logits = None

        # Create layers 0 to second-last.
        for size in hiddens[:-1]:
            layers.append(
                SlimFC(
                    in_size=prev_layer_size,
                    out_size=size,
                    initializer=normc_initializer(1.0),
                    activation_fn=activation,
                )
            )
            prev_layer_size = size

        # The last layer is adjusted to be of size num_outputs, but it's a
        # layer with activation.
        if no_final_linear and num_outputs:
            layers.append(
                SlimFC(
                    in_size=prev_layer_size,
                    out_size=num_outputs,
                    initializer=normc_initializer(1.0),
                    activation_fn=activation,
                )
            )
            prev_layer_size = num_outputs
        # Finish the layers with the provided sizes (`hiddens`), plus -
        # iff num_outputs > 0 - a last linear layer of size num_outputs.
        else:
            if len(hiddens) > 0:
                layers.append(
                    SlimFC(
                        in_size=prev_layer_size,
                        out_size=hiddens[-1],
                        initializer=normc_initializer(1.0),
                        activation_fn=activation,
                    )
                )
                prev_layer_size = hiddens[-1]
            if num_outputs:
                self._logits = SlimFC(
                    in_size=prev_layer_size,
                    out_size=num_outputs,
                    initializer=normc_initializer(0.01),
                    activation_fn=None,
                )
            else:
                self.num_outputs = ([int(np.product(obs_space.shape))] + hiddens[-1:])[
                    -1
                ]

        # Layer to add the log std vars to the state-dependent means.
        if self.free_log_std and self._logits:
            self._append_free_log_std = AppendBiasLayer(num_outputs)

        self._hidden_layers = nn.Sequential(*layers)

        self._value_branch_separate = None
        if not self.vf_share_layers:
            # Build a parallel set of hidden layers for the value net.
            prev_vf_layer_size = int(np.product(obs_space.shape))
            vf_layers = []
            for size in hiddens:
                vf_layers.append(
                    SlimFC(
                        in_size=prev_vf_layer_size,
                        out_size=size,
                        activation_fn=activation,
                        initializer=normc_initializer(1.0),
                    )
                )
                prev_vf_layer_size = size
            self._value_branch_separate = nn.Sequential(*vf_layers)

        self._value_branch = SlimFC(
            in_size=prev_layer_size,
            out_size=1,
            initializer=normc_initializer(0.01),
            activation_fn=None,
        )
        # Holds the current "base" output (before logits layer).
        self._features = None
        # Holds the last input, in case value branch is separate.
        self._last_flat_in = None

    @override(TorchModelV2)
    def forward(
        self,
        input_dict: Dict[str, TensorType],
        state: List[TensorType],
        seq_lens: TensorType,
    ) -> (TensorType, List[TensorType]):
        obs = input_dict["obs_flat"].float()
        self._last_flat_in = obs.reshape(obs.shape[0], -1)
        self._features = self._hidden_layers(self._last_flat_in)
        logits = self._logits(self._features) if self._logits else self._features
        if self.free_log_std:
            logits = self._append_free_log_std(logits)
        return logits, state

    @override(TorchModelV2)
    def value_function(self) -> TensorType:
        assert self._features is not None, "must call forward() first"
        if self._value_branch_separate:
            out = self._value_branch(
                self._value_branch_separate(self._last_flat_in)
            ).squeeze(1)
        else:
            out = self._value_branch(self._features).squeeze(1)
        return out

#from torch_scatter import scatter
class TorchCustomLossModel(TorchModelV2, nn.Module):
    """PyTorch version of the CustomLossModel above."""

    def __init__(
        self, obs_space, action_space, num_outputs, model_config, name, input_files
    ):
        super().__init__(obs_space, action_space, num_outputs, model_config, name)
        nn.Module.__init__(self)

        self.input_files = input_files
        # Create a new input reader per worker.
        self.reader = JsonReader(self.input_files)
        self.fcnet = TorchFC(
            self.obs_space, self.action_space, num_outputs, model_config, name="fcnet"
        )

    @override(ModelV2)
    def forward(self, input_dict, state, seq_lens):
        # Delegate to our FCNet.
        return self.fcnet(input_dict, state, seq_lens)

    @override(ModelV2)
    def value_function(self):
        # Delegate to our FCNet.
        return self.fcnet.value_function()

    @override(ModelV2)
    def custom_loss(self, policy_loss, loss_inputs):
        """Calculates a custom loss on top of the given policy_loss(es).

        Args:
            policy_loss (List[TensorType]): The list of already calculated
                policy losses (as many as there are optimizers).
            loss_inputs: Struct of np.ndarrays holding the
                entire train batch.

        Returns:
            List[TensorType]: The altered list of policy losses. In case the
                custom loss should have its own optimizer, make sure the
                returned list is one larger than the incoming policy_loss list.
                In case you simply want to mix in the custom loss into the
                already calculated policy losses, return a list of altered
                policy losses (as done in this example below).
        """
        # Get the next batch from our input files.
        batch = self.reader.next()

        # Define a secondary loss by building a graph copy with weight sharing.
        obs = restore_original_dimensions(
            torch.from_numpy(batch["obs"]).float().to(policy_loss[0].device),
            self.obs_space,
            tensorlib="torch",
        )
        logits, _ = self.forward({"obs": obs}, [], None)

        # Compute the IL loss.
        action_dist = TorchCategorical(logits, self.model_config)
        imitation_loss = torch.mean(
            -action_dist.logp(
                torch.from_numpy(batch["actions"]).to(policy_loss[0].device)
            )
        )
        self.imitation_loss_metric = imitation_loss.item()
        self.policy_loss_metric = np.mean([loss.item() for loss in policy_loss])

        # Add the imitation loss to each already calculated policy loss term.
        # Alternatively (if custom loss has its own optimizer):
        # return policy_loss + [10 * self.imitation_loss]
        return [loss_ + 10 * imitation_loss for loss_ in policy_loss]

    def metrics(self):
        return {
            "policy_loss": self.policy_loss_metric,
            "imitation_loss": self.imitation_loss_metric,
        }

# hard-coded input
# input for factors with types
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


class FactorModule(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim=64):
        super(FactorModule, self).__init__()
        # Example architecture, adjust as needed
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),  # Arbitrary hidden layer size
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.network(x)

class FactorGraphRL(nn.Module):
    def __init__(self, factors, embed_size = 10):
        super(FactorGraphRL, self).__init__()

        self.factors = nn.ModuleDict()
        #self.embeddings = {}
        self.factor_dict = {}

        for factor in factors:
            self.factor_dict[factor['factor_name']] = []

            for var_t in factor['used_state_variables']:
                input_vars = var_t['name']
                self.factor_dict[factor['factor_name']].append(input_vars)

            # calculate input total dim and output total dim for the factor
            input_dim_t = len(factor['used_state_variables'])
            output_dim_t = len(factor['modified_state_variables'])

            # add factor (FactorModule) to factors dict with factor_name
            self.factors[factor['factor_name']] = FactorModule(input_dim_t, output_dim_t)


    def forward(self, inputs):
        # Assuming `inputs` is a dict with state_variable_name: Tensor pairs
        outputs = {}
        for factor_name, module in self.factors.items():
            # Extract input variables for this factor
            input_tensors = [inputs[var_name] for var_name in self.factor_dict[factor_name]]

            # Concatenate inputs if more than one, else use the single tensor directly
            input_tensor = torch.cat(input_tensors, dim=-1) if len(input_tensors) > 1 else input_tensors[0]
            outputs[factor_name] = module(input_tensor)
        # Implement aggregation and further processing as needed
        # Example: Summing up outputs, but this depends on your specific application
        #final_output = torch.sum(torch.stack(list(outputs.values())), dim=0)
        #return final_output

        return outputs


if __name__ == "__main__":
    embed_size = 10
    model = FactorGraphRL(factors, embed_size)
    x = torch.ones(12, 1)

    inputs = {}
    cnt = 0
    for factor in factors:
        for item in factor['used_state_variables']:
            inputs[item['name']] = x[cnt]
            cnt += 1
    assert(cnt == x.shape[0])

    r = model(inputs)
