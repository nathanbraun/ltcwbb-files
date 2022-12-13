import requests
import json
from pandas import DataFrame, Series
import pandas as pd

#######
# teams
#######

# after looking at url in browser, get what you need in python
teams_url = 'https://statsapi.mlb.com/api/v1/teams'
teams_resp = requests.get(teams_url)

teams_json = teams_resp.json()

# with open('./data/json/teams.json') as f:
#     teams_json = json.load(f)

teams_json
teams_json.keys()

type(teams_json['teams'])

len(teams_json['teams'])

teams_json['teams'][0]

wahoo_nested = teams_json['teams'][0]
wahoo_flat = {key: value for key, value in wahoo_nested.items()
              if type(value) is not dict}

wahoo_flat

wahoo_nested['league']

wahoo_flat['league_name'] = wahoo_nested['league']['name']
wahoo_flat['league_id'] = wahoo_nested['league']['id']

wahoo_flat['sport_id'] = wahoo_nested['sport']['id']
wahoo_flat['division_id'] = wahoo_nested['division']['id']
wahoo_flat['venue_id'] = wahoo_nested['venue']['id']

wahoo_flat

# above code is good, but will throw errors with missing league, sport,
# division, venue fields

# australia example:
aus = teams_json['teams'][27]
aus

# will give us errors
# aus['league']['name']
# aus['league']['id']
# aus['division']['id']

aus.get('league', {}).get('name')
aus.get('league', {}).get('id')
aus.get('division', {}).get('id')

def flatten_team(nested):
    flat = {key: value for key, value in nested.items() if type(value) is not dict}

    flat['league_name'] = nested.get('league', {}).get('name')
    flat['league_id'] = nested.get('league', {}).get('id')
    flat['sport_id'] = nested.get('sport', {}).get('id')
    flat['venue_id'] = nested.get('venue', {}).get('id')
    flat['division_id'] = nested.get('division', {}).get('id')

    return flat

df_teams = DataFrame([flatten_team(x) for x in teams_json['teams']])

df_teams.head()

df_teams['league_name'].value_counts().head(15)

df_mlb = df_teams.loc[((df_teams['league_name'] == 'American League') | 
                       (df_teams['league_name'] == 'National League'))]

df_mlb.head()

# rosters
rosters_url = 'https://statsapi.mlb.com/api/v1/teams/112/roster'
rosters_resp = requests.get(rosters_url)
rosters_json = rosters_resp.json()

# with open('./data/json/rosters.json') as f:
#     rosters_json = json.load(f)

rosters_json['roster']

aa = rosters_json['roster'][0]

aa

aa_flat = {}
aa_flat['person_id'] = aa.get('person', {}).get('id')
aa_flat['name'] = aa.get('person', {}).get('fullName')
aa_flat['active'] = aa.get('status', {}).get('description')
aa_flat['jersey'] = aa.get('jerseyNumber')
aa_flat['position'] = aa.get('position', {}).get('name')

aa_flat

def flatten_player(nested):
    flat = {}
    flat['person_id'] = nested.get('person', {}).get('id')
    flat['name'] = nested.get('person', {}).get('fullName')
    flat['active'] = nested.get('status', {}).get('description')
    flat['jersey'] = nested.get('jerseyNumber')
    flat['position'] = nested.get('position', {}).get('name')
    return flat

cubs_roster_flat = [flatten_player(x) for x in rosters_json['roster']]

df_cubs = DataFrame(cubs_roster_flat)

df_cubs.head()

def get_roster_by_team(team_id):
    rosters_url = f'https://statsapi.mlb.com/api/v1/teams/{team_id}/roster'
    rosters_resp = requests.get(rosters_url)
    rosters_json = rosters_resp.json()

    rosters_flat = [flatten_player(x) for x in rosters_json['roster']]
    df = DataFrame(rosters_flat)
    df['team_id'] = team_id
    return df

df_angels = get_roster_by_team(108)
df_angels.head()

rosters_5_teams = pd.concat(
    [get_roster_by_team(x) for x in df_mlb['id'].head(5)], ignore_index=True)

df_mlb[['id', 'name']].head(5)

rosters_5_teams['team_id'].value_counts()
rosters_5_teams.sample(20)

