"""
Answers to the end of chapter exercises for Pandas chapter.

Questions with written (not code) answers are inside triple quotes.
"""
import pandas as pd
from os import path
import numpy as np

###############################################################################
# PANDAS BASICS
###############################################################################

# DATA_DIR = '/Users/nathan/fantasybook/data'
DATA_DIR =  '/Users/nathanbraun/fantasymath/fantasybook-baseball/data'

#######
# 3.0.1
#######
dfp = pd.read_csv(path.join(DATA_DIR, '2018-season', 'pitches.csv'))

#######
# 3.0.2
#######
dfp50 = dfp.sort_values('ERA').head(50)
dfp50.head()

#######
# 3.0.3
#######
dfp.sort_values('nameFirst', ascending=False, inplace=True)
dfp.head()

# Note: if this didn't work when you printed it on a new line in the REPL you
# probably forgot the `inplace=True` argument.

#######
# 3.0.4
#######
type(dfp.sort_values('W'))

#######
# 3.0.5
#######
# a
dfp_simple = dfp[['nameFirst', 'nameLast', 'W', 'L', 'ERA']]

# b
dfp_simple = dfp_simple[['nameLast', 'nameFirst', 'ERA', 'W', 'L']]

# c
dfp_simple['team'] = dfp['teamID']

# d
dfp.to_csv(path.join(DATA_DIR, 'problems', 'dfp_simple.txt'), sep='|')

###############################################################################
# COLUMNS
###############################################################################

#######
# 3.1.1
#######
dfb = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'atbats.csv'))

#######
# 3.1.2
#######
dfb['runs_scored'] = dfb['b_score_end'] - dfb['b_score_start']
dfb['runs_scored'].head()

#######
# 3.1.3
#######
dfb['ab_desc'] = (dfb['batter'] + ' got a ' + dfb['event'] + ' vs ' +
                 dfb['pitcher'])
dfb['ab_desc'].head()

#######
# 3.1.4
#######
dfb['final_out'] = dfb['o'] == 3
dfb[['inning', 'top', 'o', 'final_out']].head(10)

#######
# 3.1.5
#######
dfb['len_last_name'] = (dfb['pitcher']
                       .apply(lambda x: len(x.split('.')[-1])))
dfb[['pitcher', 'len_last_name']].sample(5)

#######
# 3.1.6
#######
dfb['ab_id'] = dfb['ab_id'].astype(str)

#######
# 3.1.7
#######
# a
dfb.columns = [x.replace('_', ' ') for x in dfb.columns]
dfb.head()

# b
dfb.columns = [x.replace(' ', '_') for x in dfb.columns]
dfb.head()

#######
# 3.1.8
#######
# a
dfb['run_portion'] = dfb['runs_scored']/dfb['b_score_end']
dfb['run_portion'].head()

# b
"""
`'run_portion'` is runs scored this at bat divided by total runs scored. Since
you can't divide by 0, `'run_portion'` is missing whenever the batting team
doesn't have any runs yet.
"""

# To replace all the missing values with `-99`:
dfb['run_portion'].fillna(-99, inplace=True)
dfb['run_portion'].head()

#######
# 3.1.9
#######
dfb.drop('run_portion', axis=1, inplace=True)
dfb.head()

# If you forget the `axis=1` Pandas will try to drop the *row* with the
# index value `'run_portion'`. Since that doesn't exist, it'll throw an error.

# Without the `inplace=True`, Pandas just returns a new copy of `dfb` without the
# `'run_portion'` column. Nothing happens to the original `dfb`, though we
# could reassign it if we wanted like this:

# alternative to inplace=True
# dfb = dfb.drop('run_portion', axis=1)  # alt to inplace

###############################################################################
# BUILT-IN FUNCTIONS
###############################################################################
#######
# 3.2.1
#######
dfb = pd.read_csv(path.join(DATA_DIR, '2018-season', 'atbats.csv'))

#######
# 3.2.2
#######
dfb['extra_base1'] = dfb['2B'] + dfb['3B'] + dfb['HR']

dfb['extra_base2'] = dfb[['2B', '3B', 'HR']].sum(axis=1)

(dfb['extra_base1'] == dfb['extra_base2']).all()

#######
# 3.2.3
#######

# a
dfb[['H', 'SO', 'HR']].mean()

# H     70.223485
# SO    65.632576
# HR     9.717803

# b
((dfb['H'] >= 150) & (dfb['SO'] >= 150)).sum()  # 6

# c
(((dfb['H'] >= 150) & (dfb['SO'] >= 150)).sum()/  # 6/46 = 13.04%
(dfb['H'] >= 150).sum())

# d
dfb['AB'].max()  # 664

# e
dfb['team'].value_counts()

###############################################################################
# FILTERING
###############################################################################
#######
# 3.3.1
#######
dfp = pd.read_csv(path.join(DATA_DIR, '2018-season', 'pitches.csv'))

#######
# 3.3.2
#######
# a
dfp_nyy1 = dfp.loc[dfp['teamID'] == 'NYN', ['nameFirst', 'nameLast', 'G', 'ERA']]
dfp_nyy1.head()

# b
dfp_nyy2 = dfp.query("teamID == 'NYN'")[['nameFirst', 'nameLast', 'G', 'ERA']]
dfp_nyy2.head()

#######
# 3.3.3
#######
dfp_no_nyy = dfp.loc[dfp['teamID'] != 'NYN', ['nameFirst', 'nameLast', 'G', 'ERA']]
dfp_no_nyy.head()

#######
# 3.3.4
#######

# a
dfp[['nameLast', 'lgID']].duplicated().any()  # yes there are

dfp[['nameLast', 'lgID']].duplicated().sum()

# b
# flags ALL dups (not just 2nd) because passing keep=False
dups = dfp[['nameLast', 'lgID']].duplicated(keep=False)

dfp_dups = dfp.loc[dups]
dfp_no_dups = dfp.loc[~dups]

#######
# 3.3.5
#######
dfp['era_description'] = np.nan
dfp.loc[dfp['ERA'] <= 2.5, 'era_description'] = 'stud'
dfp.loc[dfp['ERA'] > 5, 'era_description'] = 'scrub'
dfp[['ERA', 'era_description']].sample(5)


#######
# 3.3.6
#######
# a
dfp_no_desc1 = dfp.loc[dfp['era_description'].isnull()]

# b
dfp_no_desc2 = dfp.query("era_description.isnull()")

###############################################################################
# GRANULARITY
###############################################################################
#######
# 3.4.1
#######
"""
Usually you can only shift your data from more (pitch) to less (at bat)
granular, which necessarily results in a loss of information. If I go from
knowing how fast Justin Verlander pitched on every single pitch to just knowing
the result of each at bat (hit, strikeout, etc), that's a loss of information.
"""

#######
# 3.4.2
#######

# a
dfb = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'atbats.csv'))

# b
(dfb.groupby(['g_id', 'batter_id', 'batter'])['hit'].sum())

# c
dfb['is_double'] = dfb['event'] == 'Double'
(dfb.groupby('g_id')['is_double'].mean())

# d
(dfb.groupby(['g_id', 'batter_id'])['homerun'].sum() >= 2).mean()

#######
# 3.4.3
#######

# a
dfb2 = dfb.groupby(['g_id', 'batter_id']).agg(
    total_hrs = ('homerun', 'sum'),
    total_hits = ('hit', 'sum'),
    batter = ('batter', 'first'))

dfb2.head()

# b
dfb2.reset_index(inplace=True)
dfb2.head()

# c
dfb2['phr'] = dfb2['total_hrs']/dfb2['total_hits']

# d
dfb2.groupby('batter_id').count()

"""
Count counts the number of non missing (non `np.nan`) values. This is different
than `sum` which adds up the values in all of the columns. The only time
`count` and `sum` would return the same thing is if you had a column filled
with 1s without any missing values.
"""

#######
# 3.4.4
#######
"""
Stacking is when you change the granularity in your data, but shift information
from rows to columns (or vis versa) so it doesn't result in any loss on
information.
"""

###############################################################################
# COMBINING DATAFRAMES
###############################################################################
#######
# 3.5.1
#######
# a
df_hit = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'hits.csv'))
df_out = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'outs.csv'))
df_other = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'other.csv'))

# b
df_comb1 = pd.merge(df_hit, df_out, how='outer')
df_comb1 = pd.merge(df_comb1, df_other, how='outer')

df_comb1 = df_comb1.fillna(0)

# c
df_comb2 = pd.concat([df_hit.set_index('batter'), df_out.set_index('batter'),
                      df_other.set_index('batter')], axis=1)
df_comb2 = df_comb2.fillna(0)

# d
"""
Which is better is somewhat subjective, but I generally prefer `concat` when
combining three or more DataFrames because you can do it all in one step.

Note `merge` gives a little more fine grained control over how you merge (left,
or outer) vs `concat`, which just gives you inner vs outer.

Note also we have to set the index equal batter before concating.
"""

########
# 3.5.2a
########
outfield = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'outfield.csv'))
infield = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'infield.csv'))
pitcher = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'pitcher.csv'))

# b
df1 = pd.concat([outfield, infield, pitcher], ignore_index=True)

# c
df2 = pd.concat([x.set_index('batter') for x in [outfield, infield, pitcher]])

#######
# 3.5.3
#######
# a
dfb = pd.read_csv(path.join(DATA_DIR, '2018-season', 'atbats.csv'))

# b
for lg in ['AL', 'NL']:
    (dfb
     .query(f"lg == '{lg}'")
     .to_csv(path.join(DATA_DIR, f'atbats_{lg}.csv'), index=False))


# c
dfb2 = pd.concat([pd.read_csv(path.join(DATA_DIR, f'atbats_{lg}.csv'))
                  for lg in ['AL', 'NL']], ignore_index=True)

