import pandas as pd
from pandas import DataFrame
import statsapi

box_score = statsapi.boxscore(565997)
print(box_score)

standings = statsapi.standings(leagueId=104, date='10/05/2022')
print(standings)

# standings_data
sd = statsapi.standings_data(leagueId="103,104", season=2022)

# with open('./data/json/standings.json') as f:
#     sd = json.load(f)

type(sd)
sd.keys()

div201 = sd[201]

div201.keys()
div201

div201['teams']

def process_division(div):
    div_df = DataFrame(div['teams'])
    div_df['division'] = div['div_name']
    return div_df

process_division(div201)

team_df = pd.concat([process_division(value) for _, value in sd.items()],
                    ignore_index=True)

team_df[['name', 'team_id', 'w', 'l', 'gb', 'division']]

## lookup_player does NOT work like this, though it'd be easier to understand
## what you were doing if it did:
# statsapi.lookup_player(team_id=147)
# statsapi.lookup_player(last_name="Abreu")
# statsapi.lookup_player(jersey=84)
# statsapi.lookup_player(position="P")

yankee_roster = statsapi.lookup_player(147)
yankee_roster[:2]

def process_player(player):
    # dict comprehension to only keep "flat" fields of player
    # i.e. -- NOT including if value is a dict
    flat_dict = {key: value for key, value
        in player.items()
        if type(value) is not dict}

    # adding fields that ARE nested to dict
    # note "get" syntax to avoid KeyError if field is missing
    flat_dict['position'] = player.get('primaryPosition', {}).get('abbreviation')
    flat_dict['team'] = player.get('currentTeam', {}).get('id')

    return flat_dict

yankee_df = DataFrame([process_player(player) for player in yankee_roster])
yankee_df.head()

def roster_by_team(team_id):
    roster_list = statsapi.lookup_player(team_id)
    return DataFrame([process_player(player) for player in roster_list])

team_df[['name', 'team_id', 'w', 'l', 'gb', 'division']].head()

bluejay_df = roster_by_team(141)
bluejay_df.head()

player_df = pd.concat([roster_by_team(team_id) for team_id in
                          team_df['team_id'].head()], ignore_index=True)

player_df.sample(20)

tg_id = 607192
tg_stats = statsapi.player_stat_data(tg_id, group='pitching')

type(tg_stats['stats'])
len(tg_stats['stats'])

tg_stats['stats'][0]

def proc_stats1(player):

    # top level stats field -- list
    stats = player['stats'][0]

    # actual stats to return
    to_return = stats.get('stats', {})

    # add other info
    to_return['season'] = stats.get('season')
    to_return['type'] = stats.get('type')

    return to_return

proc_stats1(tg_stats)

def proc_stats2(player):

    # top level stats field -- list
    stat_list = player.get('stats', [])
    any_stats = len(stat_list) > 0

    if not any_stats:
        return {'player_id': player.get('id')}
    else:
        stats = stat_list[0]
        to_return = stats.get('stats', {})
        # add other info
        to_return['season'] = stats.get('season')
        to_return['type'] = stats.get('type')

        # add player info
        to_return['player_id'] = player.get('id')

        return to_return


def stats_by_player(player_id, group):
    player_stats = statsapi.player_stat_data(player_id, group=group)
    return proc_stats2(player_stats)

pitcher_df = DataFrame([stats_by_player(x, 'pitching') for x in
                       player_df.query("position == 'P'")['id'].head(20)])

pitcher_df.head()

pitcher_df.query("type.notnull()").head(10)


batting_df = DataFrame([stats_by_player(x, 'batting') for x in
                       player_df.query("position != 'P'")['id'].head(20)])

batting_df[['player_id', 'gamesPlayed', 'runs', 'doubles', 'triples',
    'homeRuns', 'strikeOuts', 'hits', 'avg', 'atBats', 'obp', 'slg', 'ops']]

