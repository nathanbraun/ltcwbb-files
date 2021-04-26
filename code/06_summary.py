import pandas as pd
import seaborn as sns
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathan/baseball-book/data'

###############
# distributions
###############

df = pd.read_csv(path.join(DATA_DIR, '100-game-sample', 'pitches.csv'))

# median speed of verlander's fastball
df.query("pitcher == 'J.Verlander' & pitch_type == 'FF'")['mph'].median()

# summary stats
df['mph'].quantile(.9)
df.query("pitch_type == 'FF'")['mph'].quantile(.9)
df[['mph', 'spin_rate']].describe()

# densitiy plots with python

# all on one line
g = sns.FacetGrid(df).map(sns.kdeplot, 'mph', shade=True)

# on seperate lines so it's clearer it's a two step process
g = (sns.FacetGrid(df, aspect=1.75)
     .map(sns.kdeplot, 'mph', shade=True))

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Pitch Speed Distribution')
g.savefig('./plots/pitch_density.png')

# let's limit our data to the most common pitches
df_common = df.query("pitch_type in ('FF', 'SL', 'CH', 'FT', 'CU', 'SI', 'FC')")

# density plot of pitch speed by type
g = (sns.FacetGrid(df_common, hue='pitch_type', aspect=1.75)
     .map(sns.kdeplot, 'mph', shade=True))

g.add_legend()
g.set(xlim=(65, 105))

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Pitch Speed by Type')
g.savefig('./plots/pitch_speed_by_type.png')

# density plot of pitch speed by type and strikes
g = (sns.FacetGrid(df_common, hue='pitch_type', col='s')
     .map(sns.kdeplot, 'mph', shade=True))
g.add_legend()
g.set(xlim=(65, 105))

g.fig.subplots_adjust(top=0.8)
g.fig.suptitle('Distribution of Pitch Speed by Type and N of Strikes')
g.savefig('./plots/pitch_speed_by_type_strikes.png')

# swap the hue and col arguments
# note the col_wrap=3 argument is just telling seaborn to start a new row after
# 3 columns
g = (sns.FacetGrid(df_common, hue='s', col='pitch_type', col_wrap=3)
     .map(sns.kdeplot, 'mph'))
g.add_legend()
g.set(xlim=(68,105))

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Pitch Speed by Type and N of Strikes')
g.savefig('./plots/pitch_speed_by_type_strikes_swapped.png')


# full count
# note: aspect, height, etc are purely aesthetic, we'll cover them below
g = (sns.FacetGrid(df_common, col='s', row='b', hue='pitch_type', aspect=1.75,
                   height=2) .map(sns.kdeplot, 'mph', shade=True))
g.add_legend()
g.set(xlim=(65,105))

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Pitch Speed by Type and Count')
g.savefig('./plots/pitch_speed_by_type_full_count.png')


# example of reshaping data to get it into the shape we want
# thinking about seaborn: specify seperate columns for columns, hue (color),
# thing we're plotting (points)
# so we need points in one column, then another type for scoring type
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
g = (sns.FacetGrid(games_long, hue='location', aspect=1.75)
     .map(sns.kdeplot, 'final_score', shade=True))
g.add_legend()
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distributions of Runs by Home/Away')
g.savefig('./plots/runs_by_home_away.png')

#################################
# relationships between variables
#################################

# speed vs spin
g = sns.relplot(x='mph', y='spin_rate', data=df, s=25)
g.set(ylim=(0, 3500), xlim=(65,105))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Pitch Speed vs Spin')

# speed vs spin colored yb pitch type
g = sns.relplot(x='mph', y='spin_rate', hue='pitch_type', data=df_common, s=25)
g.set(ylim=(0, 3500), xlim=(65,105))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Pitch Speed vs Spin - Pitch Type')

# number of strikes
g = sns.relplot(x='mph', y='spin_rate', hue='pitch_type', col='s', row='b',
                data=df_common, s=25)
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
                data=df_common.query("i <=9"))

df.loc[(df['pitch_type'] == 'CU') & (df['i'] == 2),
       ['pitcher', 'batter', 'i', 'pitch_type', 'mph']].sample(5)

# max points by week and position
max_speed_by_pitch_type_i = (df_common
                             .query("i <=9")
                             .groupby(['pitch_type', 'i'], as_index=False)
                             ['mph'].max())

g = sns.relplot(x='i', y='mph', kind='line', hue='pitch_type',
                data=max_speed_by_pitch_type_i)

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Max Points by Week and Position")

# speed by player and week
top20_pitchers = df['pitcher'].value_counts().head(20).reset_index()
top20_pitchers.columns = ['pitcher', 'n']

g = sns.relplot(x='i', y='mph', kind='line', hue='pitch_type', col='pitcher',
                col_wrap=4, height=2, data=pd.merge(df_common.query("i <=9"),
                                                    top20_pitchers))

g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Speed by Pitcher, Pitch Type, Inning")

##############
# plot options
##############

# basic plot
g = (sns.FacetGrid(df_common, hue='s', col='pitch_type')
    .map(sns.kdeplot, 'mph'))

# wrapping columns
g = (sns.FacetGrid(df_common, col='pitch_type', hue='s', col_wrap=2, aspect=2, height=3)
     .map(sns.kdeplot, 'mph', shade=True))

g.fig.subplots_adjust(top=0.9) # adding a title
g.fig.suptitle('Distribution of Pitch Speeds by Type, Strikes')

(g.set_xlabels('MPH') # modifying axis
  .set_ylabels('Density')
  .add_legend()  # adding legend
  .savefig('speed_by_type_strike.png'))  # saving

# verlander plot in book
g = (sns.FacetGrid(df.query("pitcher == 'J.Verlander' & pitch_type == 'FF'"), aspect=1.75)
     .map(sns.kdeplot, 'mph', shade=True))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Pitch Speed Distribution - Verlander's Four-seam Fastball")
g.savefig('./plots/pitch_density_verlander.png')


# 0.11
g = (sns.FacetGrid(df_common, hue='s', col='pitch_type')
     .map(sns.kdeplot, 'mph', shade=True))
g.add_legend()
g.set(xlim=(68,105))
g.savefig('./plots/plot_options_buildup_01.png')

# 0.12
g = (sns.FacetGrid(df_common, hue='s', col='pitch_type', col_wrap=4)
     .map(sns.kdeplot, 'mph', shade=True))
g.add_legend()
g.set(xlim=(68,105))
g.savefig('./plots/plot_options_buildup_02.png')

# 0.13
g = (sns.FacetGrid(df_common, hue='s', col='pitch_type', col_wrap=3,
                   aspect=1.4, height=1.5)
     .map(sns.kdeplot, 'mph', shade=True))
g.add_legend()
g.set(xlim=(68,105))
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle('Pitch Speed Distribution by Pitch Type and N of Strikes')
g.savefig('./plots/plot_options_buildup_final.png')
