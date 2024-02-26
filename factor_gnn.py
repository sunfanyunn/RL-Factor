import torch
import torch.nn as nn
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2


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


if __name__ == "__main__:"
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