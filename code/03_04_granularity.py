import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathan/baseball-book/data'

atbats = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'atbats.csv'))

# Granularity

# Grouping
atbats.groupby('g_id').sum().head()

sum_cols = ['strikeout', 'hit', 'homerun']
atbats.groupby('g_id').sum()[sum_cols].head()

atbats.groupby('g_id').agg({'hit': 'sum', 'homerun': 'sum', 'strikeout': 'sum',
                            'ab_id': 'count'}).head()

atbats.groupby('g_id').agg(
    hit = ('hit', 'sum'),
    n_atbats = ('ab_id', 'count'),
    strikeout = ('strikeout', 'sum'),
    homerun = ('homerun', 'sum')).head()

atbats.groupby('g_id').agg({'strikeout': ['sum', 'mean']}).head()

totals_by_game_team = atbats.groupby(
    ['g_id', 'batter_team']).sum()[sum_cols].head()

totals_by_game_team

# A note on multilevel indexing
totals_by_game_team.loc[[(201800050, 'WAS'), (201800073, 'TBA')]]

# Stacking and unstacking data
ti = (atbats
      .query("inning <= 9")
      .groupby(['inning', 'batter_team'])['hit']
      .sum()
      .reset_index())

ti.sample(5)

ti_reshaped = ti.set_index(['batter_team', 'inning']).unstack()
ti_reshaped.head()

total_hits = ti_reshaped.sum(axis=1)
total_hits.head()

ti_reshaped.stack().head()
