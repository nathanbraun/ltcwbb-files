"""
Answers to the end of chapter exercises for Python chapter.

Questions with written (not code) answers are inside triple quotes.
"""

###############################################################################
# 2.1
###############################################################################
"""
a) Valid. Python programmers often start variables with `_` if they're
throwaway or temporary, short term variables.
b) Valid.
c) Not valid. Can't start with a number.
d) Valid, though convention is to split words with _, not camelCase.
e) `rb1_name`. Valid. Numbers OK as long as they're not in the first spot
f) `flex spot name`. Not valid. No spaces
g) `@home_or_away`. Not valid. Only non alphnumeric character allowed is `_`
h) `'pts_per_rec_yd'`. Not valid. A string (wrapped in quotes), not a
variable name. Again, only non alphnumeric character allowed is `_`
"""

###############################################################################
# 2.2
###############################################################################
runs = 0
runs = runs + 2
runs = runs + 5

runs # 7

###############################################################################
# 2.3
###############################################################################
def announce_pitch(player, pitch):
    return f'{player} with the {pitch}!'

announce_pitch('Kershaw', 'slider')

###############################################################################
# 2.4
###############################################################################
"""
It's a string method, so what might `islower()` in the context of a string?
I'd say it probably returns whether or not the string is lowercase.

A function "is *something*" usually returns a yes or no answer (is it
something or not), which would mean it returns a boolean.

We can test it like:
"""

'bob uecker'.islower()  # should return True
'Bob Uecker'.islower()  # should return False

###############################################################################
# 2.5
###############################################################################
def is_travisd(player):
    return player.replace("'", '').lower() == 'travis darnaud'

is_travisd('babe ruth')
is_travisd("Travis d'Arnaud")
is_travisd("TRAVIS DARNAUD")

###############################################################################
# 2.6
###############################################################################
def commentary(ba):
    if ba >= 300:
        return f'{ba} is a good ave'
    else:
        return f"{ba}'s not that good"

commentary(275)
commentary(333)

###############################################################################
# 2.7
###############################################################################

def commentary_plus(ba):
    if ba < 1:
        ba = int(ba*1000)

    # note: i reused the commentary function from above, could also redo the
    # calculation:

    # if ba >= 300:
    #     return f'{ba} is a good ave'
    # else:
    #     return f"{ba}'s not that good"

    return commentary(ba)

commentary_plus(.200)
commentary_plus(.305)

# make sure it still works on non decimals too
commentary_plus(175)
commentary_plus(370)

###############################################################################
# 2.8
###############################################################################
dodgers_roster = ['clayton kershaw', 'cody bellinger', 'mookie betts']

dodgers_roster[0:2]
dodgers_roster[:2]
dodgers_roster[:-1]
[x for x in dodgers_roster if x != 'mookie betts']
[x for x in dodgers_roster if x in ['clayton kershaw', 'cody bellinger']]

###############################################################################
# 2.9
###############################################################################
pitcher_info = {'starter': 'Kershaw', 'throws_right': False}

# a
pitcher_info['starter'] = 'Joe Kelly'
pitcher_info

# b
def toggle_throws(pitcher):
    pitcher['throws_right'] = not pitcher['throws_right']
    return pitcher

toggle_throws(pitcher_info)

###############################################################################
# 2.10
###############################################################################
"""
a) No. `'has_a_flex'` hasn't been defined.
b) No, `number_of_teams` is a variable that hasn't been defined, the key is
`'number_of_teams'`.
c) Yes.
"""

###############################################################################
# 2.11
###############################################################################
my_roster_list = ['clayton kershaw', 'mookie betts', 'cody bellinger']

# a
for x in my_roster_list:
  print(x.split(' ')[-1])

# b
{player: len(player) for player in my_roster_list}

###############################################################################
# 2.12
###############################################################################
my_roster_dict = {
    'p': 'clayton kershaw', 'rf': 'mookie betts', '1b': 'cody bellinger'}

# a
[pos for pos in my_roster_dict]

# b
[player for _, player in my_roster_dict.items()
    if player.split(' ')[-1][0] == 'b']

###############################################################################
# 2.13
###############################################################################
# a
def mapper(my_list, my_function):
  return [my_function(x) for x in my_list]

# b
list_of_atbats = [500, 410, 618, 288, 236]

mapper(list_of_atbats, lambda x: int(x*0.300))
