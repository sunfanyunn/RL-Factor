#!/bin/bash 

### skip over the envrionemtnal generation part for now
# find yours here: https://platform.openai.com/api-keys
# export OPENAI_API_KEY=
# python run_env_generation.py


# find your wandb api key here: https://wandb.ai/authorize
export WANDB_API_KEY=029e65312d09126e44b5a5912de0720e072bb9de

export TUNE_RESULT_DIR=/data2/sunfanyun/LLM-Curriculum/results
### rl training
python simple_rl_trainer.py --exp simple_flappy_bird_ppo --algo ppo --wandb --num_gpus 1 --num_workers 40 --results_dir /data2/sunfanyun/LLM-Curriculum/results
