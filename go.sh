#!/bin/bash 

### skip over the envrionemtnal generation part for now
# find yours here: https://platform.openai.com/api-keys
# export OPENAI_API_KEY=
# python run_env_generation.py


# find your wandb api key here: https://wandb.ai/authorize
export WANDB_API_KEY=

### rl training
python rl_trainer.py --exp flappy_bird_new --wandb --num_gpus 4 --num_workers 100
