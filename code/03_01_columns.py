import pandas as pd
from pandas import DataFrame, Series
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathan/baseball-book/data'

# load data
pp = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'pitches.csv'))

pp['mph_max'] = 104.3
pp[['pitcher', 'batter', 'i', 'o', 'b', 's', 'pitch_type', 'mph', 'mph_max']].head()

pp['mph_max'] = 105.1
pp[['pitcher', 'batter', 'i', 'o', 'b', 's', 'pitch_type', 'mph', 'mph_max']].head()

# Math and number columns
pp['sz_height'] = pp['sz_top'] - pp['sz_bot']
pp[['pitcher', 'batter', 'i', 'o', 'b', 's', 'sz_top', 'sz_bot',
    'sz_height']].head()

import numpy as np  # note: normally you'd import this at the top of the file

pp['distance_from_middle_of_plate'] = np.abs(pp['x0'])

pp['ln_spin_rate'] = np.log(pp['spin_rate'])

# note on sample method

pp['season'] = 2018
pp[['pitcher', 'batter', 'i', 'o', 'b', 's', 'pitch_type', 'mph',
    'season']].sample(5)

# String Columns
pp['pitcher'].str.upper().sample(5)

pp['batter'].str.replace('.', ' ').sample(5)

(pp['pitcher'] + ' throws a ' + pp['pitch_type'] + ' to ' + pp['batter']).sample(5)

pp['batter'].str.replace('.', ' ').str.lower().sample(5)

# Bool columns
pp['is_a_FF'] = (pp['pitch_type'] == 'FF')
pp[['pitcher', 'pitch_type', 'is_a_FF']].sample(5)

pp['is_a_FF_or_SL'] = (pp['pitch_type'] == 'FF') | (pp['pitch_type'] == 'SL')
pp['fast_fastball'] = (pp['pitch_type'] == 'FF') & (pp['mph'] >= 100)
pp['is_not_FF_or_SL'] = ~((pp['pitch_type'] == 'FF') | (pp['pitch_type'] == 'SL'))

(pp[['b', 's']] == 0).sample(5)

# Applying functions to columns
def is_fastball(pitch):
  """
  Takes some string named pitch ('CH', 'FF', 'FC' etc) and checks whether it's
  a fastball (cutter, four-seam, two-seam, sinker, splitter)
  """
  return pitch in ['FC', 'FF', 'FS', 'FT', 'SI']

pp['is_fastball'] = pp['pitch_type'].apply(is_fastball)

pp[['pitcher', 'is_fastball', 'pitch_type', 'mph']].sample(5)

pp['is_fastball_alternate'] = pp['pitch_type'].apply(
    lambda x: x in ['FC', 'FF', 'FS', 'FT', 'SI'])

# Dropping Columns
pp.drop('is_fastball_alternate', axis=1, inplace=True)

# Renaming Columns
pp.columns = [x.upper() for x in pp.columns]

pp.head()

pp.columns = [x.lower() for x in pp.columns]

pp.rename(columns={'i': 'inning'}, inplace=True)

# Missing data
players = pd.read_csv(path.join(DATA_DIR, '2018-season', 'players.csv'))

players['birthState'].isnull().head(10)

players[['name', 'birthCity', 'birthState', 'birthCountry']].head(10)

players['birthState'].notnull().head(10)

players['birthState'].fillna('COUNTRY HAS NO STATES').head(10)

# Changing column types
players[['name', 'debut']].head()

debut = '20140331'

year = debut[0:4]
month = debut[4:6]
day = debut[6:8]

year
month
day

# players['month'] = players['debut'].str[4:6]  # commented out since it gives an error

players['debut_month'] = players['debut'].astype(str).str[4:6]
players[['name', 'debut_month', 'debut']].head()

players['debut_month'].astype(int).head()

players.dtypes.head()
