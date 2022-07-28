import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from os import path

# change this to your data directory
# DATA100 = '/Users/nathan/baseball-book/data/100-game-sample/'
DATA100 = './data/100-game-sample/'

# this (*_nb) is a version that i made; if you saved your own version feel free
# to remove and use that
dfp = pd.read_csv(path.join(DATA100, 'pitches_w_inplay_nb.csv'))
dfb = pd.read_csv(path.join(DATA100, 'atbats.csv'))

# book picks up here

model = smf.ols(formula='inplay ~ mph + mph2', data=dfp)
results = model.fit()
results.summary2()

def prob_inplay(mph):
    b0, b1, b2 = results.params
    return (b0 + b1*mph + b2*(mph**2))

prob_inplay(85)
prob_inplay(90)
prob_inplay(95)
prob_inplay(98)

dfp['inplay_hat'] = results.predict(dfp)
dfp[['inplay', 'inplay_hat', 'mph']].sample(5)
