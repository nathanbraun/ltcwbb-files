##############
# basic python
# v0.0.3
##############

##########################
# how to read this chapter
##########################
1 + 1

##########
# comments
##########

# print the result of 1 + 1
print(1 + 1)

###########
# variables
###########
runs_scored = 4

runs_scored
3*runs_scored

runs_scored = runs_scored + 3
runs_scored

####################
# types of variables
####################

stolen_bases = 21  # int
pitch_mph = 94.4  # float

starting_p = 'Noah Syndergaard'
starting_c = "Travis d'Arnaud"

type(starting_p)

type(stolen_bases)

starters = f'{starting_p}, {starting_c}, etc.'
starters

# string methods
"it's outta here!".upper()

'BJ Upton'.replace('BJ', 'Melvin')

####################################
# How to figure things out in Python
####################################
'mike trout'.capitalize()

'  mike trout'.lstrip()

# bools
# numbers to use in our samples
team1_runs = 6
team2_runs = 4

# and these are all bools:
team1_won = team1_runs > team2_runs
team2_won = team1_runs < team2_runs
teams_tied = team1_runs == team2_runs
teams_did_not_tie = team1_runs != team2_runs

type(team1_won)
teams_did_not_tie

# error because test for equality is ==, not =
# teams_tied = (team1_pts = team2_pts)  # commented out since it throws an error

shootout = (team1_runs > 8) and (team2_runs > 8)
at_least_one_good_team = (team1_runs > 8) or (team2_runs > 8)
pitching_duel = not ((team1_runs > 2) or (team2_runs > 2))
meh = not (shootout or at_least_one_good_team or pitching_duel)

###############
# if statements
###############
if team1_won:
  message = "Nice job team 1!"
elif team2_won:
  message = "Way to go team 2!!"
else:
  message = "must have tied!"

message

#################
# container types
#################

# lists
roster_list = ['clayton kershaw', 'mookie betts', 'cody bellinger']

roster_list[0]
roster_list[0:2]
roster_list[-2:]

# dicts
roster_dict = {'P': 'clayton kershaw',
               'RF': 'mookie betts',
               'CF': 'cody bellinger'}

roster_dict['RF']
roster_dict['1B'] = 'max muncy'
roster_dict

pos = 'RF'
roster_dict[pos]

# unpacking
p, rf = ['clayton kershaw', 'mookie betts']

p = 'clayton kershaw'
rf = 'mookie betts'

# gives an error - n of variables doesn't match n items in list
# p, rf = ['clayton kershaw', 'mookie betts', 'cody bellinger']

#######
# loops
#######

# looping over a list
roster_list = ['clayton kershaw', 'mookie betts', 'cody bellinger']

roster_list_upper = ['', '', '']
i = 0
for player in roster_list:
    roster_list_upper[i] = player.title()
    i = i + 1

roster_list_upper

# loop over just the keys
for x in roster_dict:
    print(f"position: {x}")

# use the key to get the value
for x in roster_dict:
   print(f"position: {x}")
   print(f"player: {roster_dict[x]}")

# items() for direct access to key, value
for x, y in roster_dict.items():
    print(f"position: {x}")
    print(f"player: {y}")

################
# comprehensions
################

# lists
roster_list
roster_list_proper = [x.title() for x in roster_list]
roster_list_proper

roster_list_proper_alt = [y.title() for y in roster_list]

type([x.title() for x in roster_list])
[x.title() for x in roster_list][:2]

roster_last_names = [full_name.split(' ')[1] for full_name in roster_list]
roster_last_names

full_name = 'clayton kershaw'
full_name.split(' ')
full_name.split(' ')[1]

roster_c_only = [
    x for x in roster_list if x.startswith('c')]
roster_c_only

'clayton kershaw'.startswith('c')
'mookie betts'.startswith('c')
'cody bellinger'.startswith('c')

roster_c_only_title = [
    x.title() for x in roster_list if x.startswith('c')]
roster_c_only_title

# dicts
salary_per_player = {
    'clayton kershaw': 31000000,
    'mookie betts': 27000000,
    'cody bellinger': 11500000}

salary_m_per_upper_player = {
    name.upper(): salary/1000000 for name, salary in salary_per_player.items()}

sum([1, 2, 3])
sum([salary for _, salary in salary_per_player.items()])

###########
# functions
###########
len(['clayton kershaw', 'mookie betts', 'cody bellinger'])

strikes_needed = len(
    ['clayton kershaw', 'mookie betts', 'cody bellinger'])

strikes_needed
4 + len(['clayton kershaw', 'mookie betts', 'cody bellinger'])

# defining your own functions
# (Hits + Walks + Hit by Pitch) / (At Bats + Walks + Hit by Pitch + Sacrifice Flies).
def obp(atbats, hits, walks, hit_by_pitch, sac_flies):
    """
    multi line strings in python are between three double quotes

    it's not required, but the convention is to put what the fn does in one of
    these multi line strings (called "docstring") right away in function

    when you type obp? in the REPL, it shows this docstring

    this function takes number of hits, walks, atbats, hit by pitch and
    sacrifice flies and returns on base percentage
    """
    return (hits + walks + hit_by_pitch)/(atbats + walks + hit_by_pitch +
            sac_flies)

obp(5, 1, 2, 0, 0)
# print(atbats)  # commented out since it shows an error

def noisy_obp(atbats, hits, walks, hit_by_pitch, sac_flies):
    """
    this function takes number of hits, walks, atbats, hit by pitch and
    sacrifice flies and returns on base percentage

    it also prints out atbats
    """
    print(atbats)
    return (hits + walks + hit_by_pitch)/(atbats + walks + hit_by_pitch +
            sac_flies)

noisy_obp(5, 1, 2, 0, 0)

# obp(5, 1, 2)  # commented out with error

def obp_wdefault(atbats, hits=0, walks=0, hit_by_pitch=0, sac_flies=0):
    """
    this function takes number of hits, walks, atbats, hit by pitch and
    sacrifice flies and returns on base percentage
    """
    return (hits + walks + hit_by_pitch)/(atbats + walks + hit_by_pitch +
            sac_flies)

obp_wdefault(5, 1, 2)
# obp_wdefault()  # commented out since error

obp(5, 1, 2, 0, 0)
obp?

obp(hits=1, walks=2, atbats=5, hit_by_pitch=0, sac_flies=0)

obp_wdefault(5, hits=1, walks=2)

# functions can take other functions

def do_to_list(working_list, working_fn, desc):
    """
    this function takes a list, a function that works on a list, and a
    description

    it applies the function to the list, then returns the result along with
    description as a string
    """

    value = working_fn(working_list)

    return f'{desc} {value}'

def last_elem_in_list(working_list):
    """
    returns the last element of a list.
    """
    return working_list[-1]

infield = ['1B', '2B', '3B', 'P', 'C', 'SS']

do_to_list(infield, last_elem_in_list, "last element in your list:")
do_to_list([1, 2, 4, 8], last_elem_in_list, "last element in your list:")

do_to_list(infield, len, "length of your list:")

do_to_list([2, 3, 7, 1.3, 5], lambda x: 3*x[0], "first element in your list times 3 is:")

######################
# os library and path
######################

import os  # note: normally you'd import this at the top of your file

os.cpu_count()

from os import path  # again, normally you'd import this at the top

# change this to be where ever your data is
DATA_DIR = '/Users/nathan/baseball-book/data/2018-season'

path.join(DATA_DIR, 'players.csv')
