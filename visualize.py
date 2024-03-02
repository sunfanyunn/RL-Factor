import wandb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


project_name = 'pd_repeated_torch'
entity = 'stanford_autonomous_agent'
api = wandb.Api()

# List of runs you want to plot, replace these with your actual run IDs or names
runs_ids = ['084b0_00000', '084b0_00001', '084b0_00002']

# Initialize a dict to hold the data
data = {}

# Fetch the runs and their data
for run_id in runs_ids:
    run = api.run(f"{entity}/{project_name}/{run_id}")
    history = run.scan_history(keys=["episode_reward_mean"])
    rewards = [x['episode_reward_mean'] for x in history]
    data[run_id] = rewards

df_plot = pd.DataFrame([(key, idx, val) for key, lst in data.items() for idx, val in enumerate(lst)], columns=['Run ID', 'Epoch', 'Reward'])
df_plot['Reward'] = df_plot['Reward'].replace('NaN', 0)
df_plot['Run ID'] = df_plot['Run ID'].astype(str)

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_plot, x='Epoch', y='Reward', hue='Run ID')
plt.title('Training Reward Curves')
plt.xlabel('Epochs')
plt.ylabel('Reward')
plt.legend(title='Run ID')
# save plot in results/figures folder
plt.savefig('./results/figures/train_curves.png')