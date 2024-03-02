from ray.rllib.core.rl_module.rl_module import RLModuleConfig
from ray.rllib.utils.nested_dict import NestedDict
from ray.rllib.core.rl_module.torch.torch_rl_module import TorchRLModule
from ray.rllib.utils.framework import try_import_torch
import logging
from typing import Mapping, Any

torch, nn = try_import_torch()
logger = logging.getLogger(__name__)


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


class FactorGraph(nn.Module):
    def __init__(self, factors, embed_size = 10):
        super(FactorGraph, self).__init__()

        self.factors = nn.ModuleDict()
        #self.embeddings = {}
        self.factor_dict = {}

        self.variable_names = set()
        for factor in factors:
            self.factor_dict[factor['factor_name']] = []

            for var_t in factor['used_state_variables']:
                input_vars = var_t['name']
                self.factor_dict[factor['factor_name']].append(input_vars)
                self.variable_names.add(input_vars)
            
            for var_t in factor['modified_state_variables']:
                self.variable_names.add(input_vars)

            # calculate input total dim and output total dim for the factor
            input_dim_t = len(factor['used_state_variables'])
            output_dim_t = len(factor['modified_state_variables'])

            # add factor (FactorModule) to factors dict with factor_name
            self.factors[factor['factor_name']] = FactorModule(input_dim_t, output_dim_t)

        self.variable_names = list(sorted(self.variable_names))


    def forward(self, input):
        # input comes in the shape of batch_sizse, observation_size
        input_obs = {self.variable_names[i]: input[:, i] for i in range(input.shape[1])}
        return self._forward(input_obs)


    def _forward(self, inputs):
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
        final_output = torch.sum(torch.stack(list(outputs.values())), dim=0)
        return final_output
    

class FactorGraphRL(TorchRLModule):
    def __init__(self, config: RLModuleConfig) -> None:
        super().__init__(config)

    def setup(self):
        # access the factors
        factors = self.config.model_config_dict["factors"]
        self.policy = FactorGraph(factors)

    def _forward_inference(self, batch: NestedDict) -> Mapping[str, Any]:
        with torch.no_grad():
            return self._forward_train(batch)

    def _forward_exploration(self, batch: NestedDict) -> Mapping[str, Any]:
        with torch.no_grad():
            return self._forward_train(batch)

    def _forward_train(self, batch: NestedDict) -> Mapping[str, Any]:
        # batch_size x observation_shape
        action_logits = self.policy(batch["obs"])
        return {"action_dist": torch.distributions.Categorical(logits=action_logits)}


if __name__ == "__main__":
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

    embed_size = 10
    model = FactorGraph(factors)
    x = torch.ones(12, 1)

    inputs = {}
    cnt = 0
    for factor in factors:
        for item in factor['used_state_variables']:
            inputs[item['name']] = x[cnt]
            cnt += 1
    assert(cnt == x.shape[0])

    print(inputs)
    r = model(inputs)
    print(r.shape)