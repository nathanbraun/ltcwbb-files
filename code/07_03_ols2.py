import pandas as pd
import math
import numpy as np
from os import path
import statsmodels.formula.api as smf

DATA100 = '/Users/nathan/baseball-book/data/100-game-sample/'
DATA18 = '/Users/nathan/baseball-book/data/2018-season/'

dfp = pd.read_csv(path.join(DATA100, 'pitches_w_inplay_nb.csv'))
dfb = pd.read_csv(path.join(DATA100, 'atbats.csv'))
dft = pd.read_csv(path.join(DATA18, 'teams.csv'))

# book picks up here

# model:
# `runs scored in inning = b0 + b1*(whether at bat resulted in a hit)`

# need to get runs by team and inning first:
dfti = (dfb
        .groupby(['g_id', 'inning', 'pitcher_team'])
        .agg(
            runs_start = ('b_score_start', 'min'),
            runs_end = ('b_score_end', 'max'))
        .reset_index())

dfti.head()
dfti['runs'] = dfti['runs_end'] - dfti['runs_start']

# now merge it back in with at bat data
dfb = pd.merge(dfb, dfti)

model = smf.ols(formula='runs ~ hit', data=dfb)
results = model.fit()
results.summary2()

# now let's tease out hit vs not getting an out

dfb['out'] = dfb['out'].astype(int)

model = smf.ols(formula='runs ~ hit + out', data=dfb)
results = model.fit()
results.summary2()

###############
# fixed effects
###############

is_a_hit = dfb['event'].apply(
    lambda x: x in ['Single', 'Double', 'Triple', 'Home Run'])

dfb['hit_cat'] = 'Not a hit'
dfb.loc[is_a_hit, 'hit_cat'] = dfb['event']

dfb[['event', 'hit_cat']].head()

pd.get_dummies(dfb['hit_cat']).head()

model = smf.ols(formula="runs ~ C(hit_cat) + out", data=dfb)
results = model.fit()
results.summary2()

model = smf.ols(formula="runs ~ C(hit_cat, Treatment(reference='Not a hit')) + out", data=dfb)
results = model.fit()
results.summary2()

####################
# squaring variables
####################
# not actually running anything here, see the homework

#############
# natural log
#############
dft['ln_attendence'] = np.log(dft['attendance'])
dft['ln_wins'] = np.log(dft['W'])

model = smf.ols(formula='ln_attendence ~ ln_wins', data=dft)
results = model.fit()
results.summary2()

dft['playoffs'] = (dft['DivWin'] == 'Y') | (dft['WCWin'] == 'Y')

model = smf.ols(formula='ln_attendence ~ ln_wins + playoffs', data=dft)
results = model.fit()
results.summary2()

##############
# interactions
##############
dfp['spin_k'] = dfp['spin_rate']/1000

model = smf.ols(formula="inplay ~ spin_k", data=dfp)
results = model.fit()
results.summary2()

dfp['is_curveball'] = dfp['pitch_type'] == 'CU'

model = smf.ols(formula="inplay ~ spin_k + spin_k:is_curveball", data=dfp)
results = model.fit()
results.summary2()

#######
# logit
#######
model = smf.logit(formula="inplay ~ spin_k + spin_k:is_curveball",
                data=dfp.query("pitch_type not in ('EP', 'PO', 'FO')"))
logit_results = model.fit()
logit_results.summary2()

def prob_inplay_logit(spin_k, is_curveball):
    b0, b1, b2 = logit_results.params
    value = (b0 + b1*spin_k + b2*is_curveball*spin_k)
    return 1/(1 + math.exp(-value))

prob_inplay_logit(2, 0)
prob_inplay_logit(2, 1)
prob_inplay_logit(3, 0)
prob_inplay_logit(3, 1)
