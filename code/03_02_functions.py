import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathan/baseball-book/data'

atbats = pd.read_csv(path.join(DATA_DIR, '2018-season', 'atbats.csv'))

atbats.mean()
atbats.max()

# Axis
atbats[['G', 'AB', 'R', 'H', 'HR']].mean(axis=0)
atbats[['G', 'AB', 'R', 'H', 'HR']].mean(axis=1).head()

atbats['1B'] = atbats['H'] - atbats[['2B', '3B', 'HR']].sum(axis=1)
atbats[['name', '1B']].head()

# Summary functions on boolean columns
pp = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'pitches.csv'))
pp['fast_4seam'] = (pp['pitch_type'] == 'FF') & (pp['mph'] >= 100)

pp['fast_4seam'].mean()
pp['fast_4seam'].sum()

(pp['mph'] >= 104).any()
(pp['mph'] >= 60).all()

(atbats[['H', 'SO']] > 200).any(axis=1)

(atbats[['H', 'SO']] > 200).any(axis=1).sum()

(atbats[['H', 'SO']] > 200).all(axis=1).sum()

(atbats[['H', 'SO']] > 150).all(axis=1).sum()

# Other misc built-in summary functions
pp['pitch_type'].value_counts()

pp['pitch_type'].value_counts(normalize=True)

pd.crosstab(pp['i'], pp['pitch_type']).head(9)
