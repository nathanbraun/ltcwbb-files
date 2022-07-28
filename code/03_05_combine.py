import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathan/baseball-book/data'
DATA_DIR = './data'

pg = pd.read_csv(
    path.join(DATA_DIR, '100-game-sample', 'game-player.csv'))  # player-game
games = pd.read_csv(
    path.join(DATA_DIR, '100-game-sample', 'games.csv'))  # game info
players = pd.read_csv(
    path.join(DATA_DIR, '100-game-sample', 'players.csv'))  # game info

# things to care about while merging:
# 1. The columns you're joining on.
pd.merge(pg, games[['g_id', 'attendance']]).sample(5)

out_df = pg[['g_id', 'batter_id', 'out', 'strikeout']]
hit_df = pg[['g_id', 'batter_id', 'hit', 'homerun']]

combined = pd.merge(out_df, hit_df, on=['g_id', 'batter_id'])
combined.head()

combined2 = pd.merge(out_df, hit_df)

# 2. Whether you're doing a one-to-one, one-to-many, or many-to-many merge
games['g_id'].duplicated().any()

pg['g_id'].duplicated().any()

player_names = players.rename(columns={'id': 'batter_id'})[['batter_id',
    'first_name', 'last_name']]
player_names.head(5)

player_names['batter_id'].duplicated().any()

pg['batter_id'].duplicated().any()

pd.merge(combined, player_names).head()

# pd.merge(combined, player_names, validate='1:1')  # this will fail since it's 1:m

# 3. What you do with unmatched observations
st = pd.read_csv(path.join(DATA_DIR, '2018-season', 'teams.csv'))  # player-game

top_hr = (st[['teamID', 'name', 'HR']]
          .sort_values('HR', ascending=False)
          .head(20))

top_so = (st[['teamID', 'name', 'SO']]
          .sort_values('SO', ascending=False)
          .head(20))

top_hr.shape
top_so.shape

comb_inner = pd.merge(top_hr, top_so)
comb_inner.shape

comb_left = pd.merge(top_hr, top_so, how='left')
comb_left.shape

comb_left.head(10)

comb_outer = pd.merge(top_hr, top_so, how='outer', indicator=True)
comb_outer.shape

comb_outer['_merge'].value_counts()

# More on pd.merge

hit_df.head()

players.head()

# left_on and right_on
pd.merge(hit_df, players, left_on='batter_id', right_on='id').sample(5)

max_hit_df = (hit_df
              .groupby('batter_id')
              .agg(max_hits = ('hit', 'max'),
                   max_hrs = ('homerun', 'max')))

max_hit_df.head()

pd.merge(hit_df, max_hit_df, left_on='batter_id', right_index=True).sample(5)

############
## pd.concat
############

top_hr = (st[['teamID', 'HR']]
          .sort_values('HR', ascending=False)
          .head(20)
          .set_index('teamID'))


top_so = (st[['teamID', 'SO']]
          .sort_values('SO', ascending=False)
          .head(20)
          .set_index('teamID'))

top_hr.head()
pd.concat([top_hr, top_so], axis=1).sort_index().head()

top_bb = (st[['teamID', 'BB']]
            .sort_values('BB', ascending=False)
            .head(20)
            .set_index('teamID'))

pd.concat([top_hr, top_so, top_bb], axis=1).sort_index().head()

st.set_index('teamID', inplace=True)
al_teams = st.query("lgID == 'AL'")
nl_teams = st.query("lgID == 'NL'")

al_teams.shape
nl_teams.shape

pd.concat([al_teams, nl_teams]).shape

al_reset = al_teams.reset_index()
nl_reset = nl_teams.reset_index()

al_reset.head()

pd.concat([al_reset, nl_reset]).sort_index().head()

pd.concat([al_reset, nl_reset], ignore_index=True).sort_index().head()
