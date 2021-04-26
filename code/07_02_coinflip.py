import random
from pandas import DataFrame
import statsmodels.formula.api as smf

coin = ['H', 'T']

# make empty DataFrame
df = DataFrame(index=range(100))

# now fill it with a "guess"
df['guess'] = [random.choice(coin) for _ in range(100)]

# and flip
df['result'] = [random.choice(coin) for _ in range(100)]

# did we get it right or not?
df['right'] = (df['guess'] == df['result']).astype(int)

model = smf.ols(formula='right ~ C(guess)', data=df)
results = model.fit()
results.summary2()

random.randint(1, 10)
