import pandas as pd
from os import path

DATA100 = './data/100-game-sample/'

dfp = pd.read_csv(path.join(DATA100, 'pitches.csv'))
dfb = pd.read_csv(path.join(DATA100, 'atbats.csv'))

# book picks up here
dfp.columns

dfp['mph'].describe()

dfp['mph2'] = dfp['mph'] ** 2
dfp[['mph', 'mph2']].head()

dfp[['ab_id', 'pitch_num', 'mph']].head(12)

last_pitch_ab = (dfp
                 .groupby('ab_id')
                 .agg(last_pitch_num = ('pitch_num', 'max'))
                 .reset_index())

# above: using agg to pick out names during groupby
# alternative way: use groupby, then rename

# last_pitch_ab = (dfp
#                  .groupby('ab_id')['pitch_num'].max()
#                  .reset_index()
#                  .rename(columns={'pitch_num': 'last_pitch_num'}))

last_pitch_ab.head()

dfp = pd.merge(dfp, last_pitch_ab, how='left')

dfp[['ab_id', 'pitch_num', 'mph', 'last_pitch_num']].head(12)

dfp['is_last_pitch'] = dfp['pitch_num'] == dfp['last_pitch_num']

dfp[['ab_id', 'pitch_num', 'mph', 'last_pitch_num', 'is_last_pitch']].head(5)

events_not_in_play = ['strikeout', 'walk', 'hit by pitch', 'intent walk',
                      'strikeout - dp', 'batter interference']

dfb['atbat_inplay'] = (~dfb['event']
        .apply(lambda x: x.lower() in events_not_in_play))

dfb['atbat_inplay'].mean()

dfp = pd.merge(dfp, dfb[['ab_id', 'atbat_inplay']])
dfp[['ab_id', 'pitch_num', 'mph', 'is_last_pitch', 'atbat_inplay']].head()

dfp['inplay'] = dfp['is_last_pitch'] & dfp['atbat_inplay']

dfp[['inplay', 'mph', 'mph2']].head()

dfp['inplay'] = dfp['inplay'].astype(int)

dfp[['inplay', 'mph', 'mph2']].head()

# save this for later
dfp.to_csv(path.join(DATA100, 'pitches_w_inplay.csv'), index=False)
