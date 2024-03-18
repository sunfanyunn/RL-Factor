# RL-Factor

This repository aims to:

(a) train a policy on top of generated PyGame environments

(b) evaluate the trained policy on the "ground-truth" environments (the games under the directory `ple`)

We are using the PyGame environments here https://github.com/ntasfi/PyGame-Learning-Environment/tree/master

## Directory Structure
A generated PyGame environment looks like https://github.com/sunfanyunn/RL-Factor/blob/819c109a3f71d887646063a9d3e1d2223be8d906/env_design/envs/flappy_bird_test.py
It can be wrapped into a gym environment as such: https://github.com/sunfanyunn/RL-Factor/blob/819c109a3f71d887646063a9d3e1d2223be8d906/env_design/wrapped_envs/flappy_bird_gym.py
- `env_design/generated_envs`: you can find generated environments here
- `rl_train.py` contains the RL training code

You can take a quick look at how we are generating the environments (very outdated - I am developing this in another repository):
- `LLM-POMDP` contains the code for which we use to generate the environments 

refer to `go.sh` to start the training

### Miscellaneous

To fix storage location bug or Ray 2.9.2 (you might not have to do this):

change the `/data2/sunfanyun/miniconda3/lib/python3.9/site-packages/ray/tune/impl/tuner_internal.py:445` to 
```
storage_local_path = run_config.storage_path or _get_defaults_results_dir()
```
