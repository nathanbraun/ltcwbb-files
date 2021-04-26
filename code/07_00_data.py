import pandas as pd
from os import path

DATA100 = '/Users/nathan/baseball-book/data/100-game-sample/'

dfp = pd.read_csv(path.join(DATA100, 'pitches.csv'))
dfb = pd.read_csv(path.join(DATA100, 'atbats.csv'))

# book picks up here
dfp.columns

dfp['mph'].describe()

dfp['mph2'] = dfp['mph'] ** 2
dfp[['mph', 'mph2']].head()

# error: exponent is **, not ^
# dfp['mph2'] = dfp['mph'] ^ 2

dfp[['mph', 'mph2']].head()

dfb['event'].value_counts().head(15)

dfb['event'].unique()

events_not_in_play = ['strikeout', 'walk', 'hit by pitch', 'intent walk',
                      'bunt groundout', 'strikeout - dp', 'bunt pop out',
                      'batter interference']

dfb['inplay'] = (~dfb['event']
                 .apply(lambda x: x.lower() in events_not_in_play))

dfb['inplay'].mean()

dfb['ab_id'].duplicated().any()
dfp[['ab_id', 'pitch_num']].duplicated().any()

dfp[['ab_id', 'pitch_num', 'mph']].head()

dfb.query("ab_id == 2018003856")[['event', 'inplay']]

last_pitch_ab = (dfp
                 .groupby('ab_id')['pitch_num'].max()
                 .reset_index())
last_pitch_ab.head()

# this works, but we'll do it a safer way:
# dfb = pd.merge(dfb, last_pitch_ab)

dfb = pd.merge(dfb, last_pitch_ab,
               validate='1:1', how='outer', indicator=True)
assert (dfb['_merge'] == 'both').all()
dfb.drop('_merge', axis=1, inplace=True)

dfb[['ab_id', 'pitch_num', 'event', 'inplay']].head()

dfp = pd.merge(dfp, dfb[['ab_id', 'pitch_num', 'event', 'inplay']], how='left',
               indicator=True)

dfp[['ab_id', 'pitch_num', 'inplay', '_merge']].head()

dfp['inplay'] = dfp['inplay'].fillna(False)

dfp[['inplay', 'mph', 'mph2', '_merge']].head()

dfp['inplay'] = dfp['inplay'].astype(int)

dfp[['inplay', 'mph', 'mph2']].head()

# save this for later
dfp.to_csv(path.join(DATA100, 'pitches_w_inplay.csv'), index=False)
