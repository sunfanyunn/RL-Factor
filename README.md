# LLM-POMDP

- `run_env_generation.py` contains the entry point for code for using language to generate/modify a POMDP
- `game_strcture.py` contains the code for the hypergraph representation
- `rl_train.py` contains the RL training code (flappy bird for now)

refer to `go.sh` to start the training

###

To fix storage location bug or Ray 2.9.2:

change the `/data2/sunfanyun/miniconda3/lib/python3.9/site-packages/ray/tune/impl/tuner_internal.py:445`
to 
```
storage_local_path = run_config.storage_path or _get_defaults_results_dir()
```

