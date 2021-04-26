import pandas as pd
import numpy as np
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathan/baseball-book/data'

games = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'games.csv'))
games.set_index('g_id', inplace=True)

first_game_id = 201800050

# Filtering
games.loc[first_game_id]

random_game_ids = [201800050, 201801909, 201800465]

games.loc[random_game_ids]

games.loc[random_game_ids, ['home_team', 'away_team', 'date', 'attendance',
                            'elapsed_time']]

games.loc[random_game_ids, 'umpire_HP']

# Boolean indexing
is_delayed = games['delay'] > 0
is_delayed.head()

games_delayed = games.loc[is_delayed]

games_delayed[['home_team', 'away_team', 'date', 'delay']].head()

games_long_delay = games.loc[games['delay'] > 60]
games_long_delay[['home_team', 'away_team', 'date', 'delay']].head()

is_a_long_game = games['elapsed_time'] > 200

long_and_delayed = games.loc[is_a_long_game & is_delayed]
long_and_delayed[['home_team', 'away_team', 'date', 'delay',
                  'elapsed_time']].head()

# Duplicates
pp = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'pitches.csv'))

pp.shape
pp.drop_duplicates(inplace=True)
pp.shape

pp.drop_duplicates('pitch_type')[['pitch_type', 'mph', 'spin_rate', 'spin_dir']]

pp.duplicated().head()

pp.duplicated('pitch_type').head()

# Combining filtering with changing columns
pp['pitcher_type'] = np.nan
pp.loc[pp['i'] < 5, 'pitcher_type'] = 'starter'
pp.loc[(pp['i'] <= 7) & (pp['i'] >= 5), 'pitcher_type'] = 'middle reliever'
pp.loc[pp['i'] == 8, 'pitcher_type'] = 'setup'
pp.loc[pp['i'] == 9, 'pitcher_type'] = 'closer'

pd.crosstab(pp['i'], pp['pitcher_type'])

pp.drop('pitcher_type', axis=1, inplace=True)
pp.loc[pp['i'] < 5, 'pitcher_type'] = 'starter'

# Query
games.query("delay > 0").head()

games['is_delayed'] = games['delay'] > 0
games.query("is_delayed").head()

games.query("weather.str[0] == '9'")[['home_team', 'away_team', 'weather']].head()

# note: if getting an error on line above, try it with engine='python' like
# this
games.query("weather.str[0] == '9'", engine='python')[['home_team', 'away_team', 'weather']].head()
