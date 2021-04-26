import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathan/baseball-book/data'

##############
# Loading data
##############
players = pd.read_csv(path.join(DATA_DIR, '2018-season', 'players.csv'))

type(players)

##################################
# DataFrame methods and attributes
##################################
players.head()

players.columns

players.shape

#################################
# Working with subsets of columns
#################################
# A single column
players['name'].head()

type(players['name'])

players['name'].to_frame().head()
type(players['name'].to_frame().head())

# Multiple columns
players[['name', 'height', 'weight', 'debut']].head()

type(players[['name', 'height', 'weight', 'debut']])

# players['name', 'height', 'weight', 'debut'].head()  # commented out because it throws an error

##########
# Indexing
##########
players[['name', 'bats', 'throws', 'birthCountry']].head()

players.set_index('playerID').head()

# Copies and the inplace argument
players.head()  # note: playerID not the index, even though we just set it

players.set_index('playerID', inplace=True)
players.head()  # now playerID is index

# alternate to using inplace, reassign players
players = pd.read_csv(
    path.join(DATA_DIR, '2018-season', 'players.csv')) # players data
players = players.set_index('playerID')

players.reset_index().head()

#############################
# Indexes keep things aligned
#############################
players_cuba = players.loc[players['birthCountry'] == 'Cuba',
                           ['name', 'height', 'weight', 'birthCountry']]
players_cuba.head()

players_cuba.sort_values('weight', inplace=True)
players_cuba.head()

# assigning a new column
players_cuba['bats'] = players['bats']
players_cuba.head()

# has the same index as players_cuba and players
players['bats'].head()

#################
# Outputting data
#################
players_cuba.to_csv(
    path.join(DATA_DIR, '2018-season', 'players_cuba.csv'))

players_cuba.to_csv(
    path.join(DATA_DIR, '2018-season', 'players_cuba_no_index.csv'), index=False)

