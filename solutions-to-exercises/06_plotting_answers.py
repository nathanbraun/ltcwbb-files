"""
Answers to the end of chapter exercises for Summary Stats and Visualization
chapter.
"""
import pandas as pd
import seaborn as sns
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

# DATA_DIR = '/Users/nathan/fantasybook/data'
DATA_DIR = '/Users/nathanbraun/fantasymath/ltcwbb-files/data'

ab = pd.read_csv(path.join(DATA_DIR, '2018-season', 'atbats.csv'))

###############################################################################
# 6.1a
###############################################################################
g = sns.displot(ab, x='HR', kind='kde', fill=True)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of HR, 2018 Sample')
g.savefig('./solutions-to-exercises/6-1a.png')

###############################################################################
# 6.1b
###############################################################################
g = sns.displot(ab, x='HR', hue='lg', kind='kde', fill=True)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of HR by League, 2018 Sample')
g.savefig('./solutions-to-exercises/6-1b.png')

###############################################################################
# 6.1c
###############################################################################
g = sns.displot(ab, x='HR', col='lg', kind='kde', fill=True)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of HR by League, 2018 Sample')
g.savefig('./solutions-to-exercises/6-1c.png')

###############################################################################
# 6.1d
###############################################################################
g = sns.displot(ab, x='HR', col='lg', hue='lg', kind='kde', fill=True)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of HR by League, 2018 Sample')
g.savefig('./solutions-to-exercises/6-1d.png')

###############################################################################
# 6.1e
###############################################################################
g = sns.displot(ab, x='HR', col='team', hue='team', kind='kde', col_wrap=5)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of HR by Team, 2018 Sample')
g.savefig('./solutions-to-exercises/6-1e.png')

###############################################################################
# 6.2a
###############################################################################
# relationships
g = sns.relplot(x='HR', y='SO', hue='lg', data=ab)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Homeruns vs Strikeouts, 2018 Sample')
g.savefig('./solutions-to-exercises/6-2a.png')


###############################################################################
# 6.2b
###############################################################################
"""
The problem is players with more at bats get more opportunities to both
strikeout and hit homeruns. So this upward sloping scatter plot cloud may be
picking that up.
"""

###############################################################################
# 6.2c
###############################################################################
# To control for that, let's look at SO and HR *per at bat*.

# basic pandas to create these
ab['SO_pab'] = ab['SO']/ab['AB']
ab['HR_pab'] = ab['HR']/ab['AB']

# look at plot again
g = sns.relplot(x='HR_pab', y='SO_pab', data=ab)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('HR per at bat vs SO per at bat, 2018 Sample')
g.savefig('./solutions-to-exercises/6-2c.png')
