#!/bin/bash -ex

### skip over the envrionemtnal generation part for now
# find yours here: https://platform.openai.com/api-keys
# export OPENAI_API_KEY=
# python run_env_generation.py


# find your wandb api key here: https://wandb.ai/authorize
export WANDB_API_KEY=029e65312d09126e44b5a5912de0720e072bb9de
export TUNE_RESULT_DIR=/data2/sunfanyun/LLM-Curriculum/results

### rl training

env_id=my_flappy_bird_state_final
results_dir=/data2/sunfanyun/LLM-Curriculum/results
algo=$1

python rl_trainer_factor.py --exp factor-baselines --env_id $env_id --algo $algo --wandb --num_gpus 1 --num_workers 40 --results_dir $results_dir
#python rl_trainer.py --exp factor-baselines --env_id $env_id --algo ppo --wandb --num_gpus 1 --num_workers 40 --results_dir $results_dir
#python rl_trainer.py --exp factor-baselines --env_id $env_id --algo impala --wandb --num_gpus 1 --num_workers 40 --results_dir $results_dir
