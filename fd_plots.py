'''Produces the fairness-discrimination plots'''
import numpy as np
import pandas as pd
import seaborn as sns
import pickle

from matplotlib import pyplot as plt

import tools
import balancers


data_dir = 'data/source/'

# Reading in the original datasets
bar = pd.read_csv(data_dir + 'bar.csv')
weed = pd.read_csv(data_dir + 'drugs.csv')
obesity = pd.read_csv(data_dir + 'obesity.csv')
park = pd.read_csv(data_dir + 'park.csv')

# And reading in the predicted probabilities
bar_probs = pickle.load(open(data_dir + 'bar_probs.pkl', 'rb'))
weed_probs = pickle.load(open(data_dir + 'weed_probs.pkl', 'rb'))
obesity_probs = pickle.load(open(data_dir + 'obesity_probs.pkl', 'rb'))
park_probs = pickle.load(open(data_dir + 'park_probs.pkl', 'rb'))

df_names = ['Bar', 'Drugs', 'Obesity', 'Parkinsons']
datasets = [bar, weed, obesity, park]
probs = [bar_probs, weed_probs, obesity_probs, park_probs]

# Defining the 4 fairness types
goals = ['odds', 'strict', 'opportunity', 'demographic_parity']
goal_names = ['Odds', 'Strict', 'Opportunity', 'Parity']

# Making the two relplots: one for micro loss, and one for macro
sns.set_style('darkgrid')
sns.set(font_scale=1)

fig, axes = plt.subplots(nrows=4, ncols=4, sharey=False)

for i, goal in enumerate(goals):
    for j, df in enumerate(datasets):
        b = balancers.MulticlassBalancer(df.y.values,
                                         df.yhat.values,
                                         df.a.values)
        grid = tools.fd_grid(b, 
                             step=.01,
                             loss='macro', 
                             goal=goal)
        tools.fd_plot(grid,
                      disc='brier',
                      goal=goal,
                      ax=axes[i, j])

# Labeling the fairness constraint types
for i, goal in enumerate(goal_names):
    plt.setp(axes[i, 0], ylabel=goal)

# Labeling the datasets
for i, ds in enumerate(df_names):
    plt.setp(axes[0, i], title=ds)

fig.set_tight_layout(True)
#fig.suptitle('Fairness vs. discrimination')
fig.supxlabel('Maximum Difference in Fairness')
fig.supylabel('Brier Score')

plt.show()
