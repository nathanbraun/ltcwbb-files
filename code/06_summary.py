import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathan/baseball-book/data'

###############
# distributions
###############

# load data
df = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'pitches.csv'))

# let's limit our data to the most common pitches
df = df.query("pitch_type in ('FF', 'SL', 'CH', 'FT', 'CU', 'SI', 'FC')")

# summary stats
df['mph'].quantile(.9)
df.query("pitch_type == 'FF'")['mph'].quantile(.9)
df[['mph', 'spin_rate']].describe()

##########
# plotting
##########

g = sns.displot(df, x='mph', kind='kde', fill=True)

# density plot of pitch speed by type
g = sns.displot(df, x='mph', kind='kde', hue='pitch_type', fill=True,
                aspect=1.75)

# density plot of pitch speed by type and strikes
g = sns.displot(df, x='mph', kind='kde', hue='pitch_type', col='s', fill=True)

# swap the hue and col arguments
# note the col_wrap=3 argument is just telling seaborn to start a new row after
# 3 columns
g = sns.displot(df, x='mph', kind='kde', hue='s', col='pitch_type', col_wrap=3)

# full count
# note: aspect, height, etc are purely aesthetic, we'll cover them below
g = sns.displot(df, kind='kde', x='mph', col='s', row='b', hue='pitch_type',
                fill=True, aspect=1.75, height=2)

# example of reshaping data to get it into the shape we want

# thinking about seaborn: specify seperate columns for columns, hue (color),
# thing we're plotting (points)
# so we need points in one column, then another type for scoring type

# load data
games = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'games.csv'))

games[['home_team', 'away_team', 'home_final_score', 'away_final_score']].head()

def home_away_df(_df, location):
    _df = _df[['date', f'{location}_team', f'{location}_final_score']]
    _df.columns = ['date', 'team', 'final_score']
    _df['location'] = location
    return _df

home_away_df(games, 'home').head()

games_long = pd.concat([
    home_away_df(games, loc) for loc in ['home', 'away']], ignore_index=True)

# now can plot points by scoring system and position
g = sns.displot(games_long, kind='kde', x='final_score', hue='location',
                fill=True, aspect=1.75)

##############
# plot options
##############

# basic plot
g = sns.displot(df, kind='kde', x='mph', hue='s', col='pitch_type')

# wrapping columns
g = sns.displot(df, kind='kde', x='mph', hue='s', col='pitch_type', col_wrap=2)

# adding a title
g.fig.subplots_adjust(top=0.9) # adding a title
g.fig.suptitle('Distribution of Pitch Speeds by Type, Strikes')

# modifying the axes
g.set(xlim=(65, 105))

# changing labels
g.set_xlabels('MPH')
g.set_ylabels('Density')

# saving
g.savefig('speed_by_type_strike.png')

#################################
# relationships between variables
#################################

# NOTE: not currently in book, coming soon

# speed vs spin
g = sns.relplot(x='mph', y='spin_rate', data=df, s=25)

g.set(ylim=(0, 3500), xlim=(65,105))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Pitch Speed vs Spin')

# speed vs spin colored yb pitch type
g = sns.relplot(x='mph', y='spin_rate', hue='pitch_type', data=df, s=25)

g.set(ylim=(0, 3500), xlim=(65,105))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Pitch Speed vs Spin - Pitch Type')

# number of strikes
g = sns.relplot(x='mph', y='spin_rate', hue='pitch_type', col='s', row='b',
                data=df, s=25)

g.set(ylim=(0, 3500), xlim=(65,105))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Pitch Speed vs Spin - Pitch Type')

# correlation
df[['spin_rate', 'mph', 'end_speed', 's']].corr()

# scatter plot of 0.54 correlation
g = sns.relplot(x='mph', y='spin_rate', data=df)

# scatter plot of 0.98 correlation
g = sns.relplot(x='mph', y='end_speed', data=df)

########################
# line plots with python
########################

# speed by inning
g = sns.relplot(x='i', y='mph', kind='line', hue='pitch_type',
                data=df.query("i <=9"))

df.loc[(df['pitch_type'] == 'CU') & (df['i'] == 2),
       ['pitcher', 'batter', 'i', 'pitch_type', 'mph']].sample(5)

# max points by week and position
max_speed_by_pitch_type_i = (df
                             .query("i <=9")
                             .groupby(['pitch_type', 'i'], as_index=False)
                             ['mph'].max())

g = sns.relplot(x='i', y='mph', kind='line', hue='pitch_type',
                data=max_speed_by_pitch_type_i)

# speed by player and week
top20_pitchers = df['pitcher'].value_counts().head(20).reset_index()
top20_pitchers.columns = ['pitcher', 'n']

g = sns.relplot(x='i', y='mph', kind='line', hue='pitch_type', col='pitcher',
                col_wrap=4, height=2, data=pd.merge(df.query("i <=9"),
                                                    top20_pitchers))
