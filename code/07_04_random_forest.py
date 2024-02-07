import pandas as pd
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from os import path

DATA100 = './data/100-game-sample/'

dfp = (pd.read_csv(path.join(DATA100, 'pitches.csv'))
       .query("pitch_type.notnull() & pitch_type not in ('FO', 'PO')"))

xvars = ['b', 's', 'o', 'mph', 'x0', 'z0', 'px', 'pz', 'spin_rate', 'spin_dir',
         'sz_bot', 'sz_top', 'pitch_num', 'end_speed', 'b_score', 'on_1b',
         'on_2b', 'on_3b']
yvar = 'pitch_type'

train, test = train_test_split(dfp, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['pitch_type_hat'] = model.predict(test[xvars])
test['correct'] = (test['pitch_type_hat'] == test['pitch_type'])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)

probs.head()

results = pd.concat([
    test[['ab_id', 'pitcher', 'batter', 'mph', 'pitch_type', 'pitch_type_hat',
          'correct']],
    probs], axis=1)

(results
 .groupby('pitch_type')[['correct'] + list(probs.columns)]
 .mean().round(2))

# cross validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, dfp[xvars], dfp[yvar], cv=10)

scores
scores.mean()

# feature importance
model.fit(dfp[xvars], dfp[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)
