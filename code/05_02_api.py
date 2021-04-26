import requests
import json
from pandas import DataFrame, Series
import pandas as pd

full_mookie_url = "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27mlb%27&active_sw=%27Y%27&name_part=%27mookie%25%27"

# requests in python are handled by library requests
resp = requests.get(full_mookie_url)

# then to turn it into json:
mookie_json = resp.json()

# can see it's just a nested dict
mookie_json

# the actual part we care about is three levels deep
mookie_data = mookie_json['search_player_all']['queryResults']['row']

# less data
mookie_url2 = "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27mlb%27&active_sw=%27Y%27&name_part=%27mookie%25%27&search_player_all.col_in=player_id,name_display_first_last,team_full,position,bats,throws"
resp2 = requests.get(mookie_url2)
mookie_json2 = resp2.json()['search_player_all']['queryResults']['row']

mookie_json2

# cool, now let's generalize this to something more flexible

# note all start with same thing
# so let's put that in a constant:
MLB_URL = 'http://lookup-service-prod.mlb.com/json/'

# and deal with the endpoint sepearately
mookie_endpoint = "/json/named.search_player_all.bam?sport_code=%27mlb%27&active_sw=%27Y%27&name_part=%27mookie%25%27"

def player_search(to_search):
    search_endpoint = f'named.search_player_all.bam?sport_code=%27mlb%27&active_sw=%27Y%27&name_part=%27{to_search}%25%27&search_player_all.col_in=player_id,name_display_first_last,team_full,position,bats,throws'
    resp = requests.get(MLB_URL + search_endpoint)
    return resp.json()['search_player_all']['queryResults']['row']

yelich = player_search('yelich')
yelich

# full name?
mike_trout = player_search('mike trout')
mike_trout

# 2+ playes?
bellingers = player_search('bellinger')  # cody and chad
bellingers

# not_a_player = player_search('asdf')  # an error

# 40 man roster
roster_url = MLB_URL + f'/named.roster_40.bam?team_id=%27158%27'
resp = requests.get(roster_url)

# df_brewers = DataFrame(resp.json()['roster_40']['queryResults']['row'])

clean_resp_text = (resp.text
                   .replace('(','')
                   .replace(')','')
                   .replace(';',''))

clean_resp_text2 = (resp.text.replace('(','').replace(')','').replace(';',''))

brewers_dict = json.loads(clean_resp_text)['roster_40']['queryResults']['row']
brewers_dict[0]

brewers_roster_df = DataFrame(brewers_dict)
brewers_roster_df.head()

json.loads(resp.text
 .replace('(','')
 .replace(')','')
 .replace(';',''))

brewers_roster_df.head(2).to_dict('records')

def clean_json(resp):
    return json.loads(resp.text
                      .replace('(','')
                      .replace(')','')
                      .replace(';',''))

def roster40(team_id):
    roster_url = MLB_URL + f'/named.roster_40.bam?team_id=%27{team_id}%27'
    resp = requests.get(roster_url)
    team_json = clean_json(resp)
    return DataFrame(team_json['roster_40']['queryResults']['row'])

brewers_roster_df = roster40(158)

def teams_by_year(year):
    teams_url = MLB_URL + f'/named.team_all_season.bam?sport_code=%27mlb%27&all_star_sw=%27N%27&sort_order=name_asc&season=%27{year}%27'
    resp = requests.get(teams_url)
    teams_json = clean_json(resp)
    return DataFrame(teams_json['team_all_season']['queryResults']['row'])

teams_2020 = teams_by_year(2020)
teams_2020.head()

teams_2020[['name_display_full', 'mlb_org_id']].head()

cubs = roster40(112)

rosters_all = pd.concat([roster40(x) for x in teams_2020['mlb_org_id']],
                        ignore_index=True)

rosters_all['player_id'].duplicated().any()

rosters_all.set_index('player_id', inplace=True)

def season_hitting_data(player_id, season=2020):
    player_url = MLB_URL + f'/named.sport_hitting_tm.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id=%27{player_id}%27&season=%27{season}%27'
    resp = requests.get(player_url)
    return clean_json(resp)['sport_hitting_tm']['queryResults']['row']

season_hitting_data(605113)

def season_hitting_row(player_id, season=2020):
    player_url = MLB_URL + f'/named.sport_hitting_tm.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id=%27{player_id}%27&season=%27{season}%27'
    resp = requests.get(player_url)
    return Series(clean_json(resp)['sport_hitting_tm']['queryResults']['row']).to_frame(player_id).T

season_hitting_row(605113)

# season_hitting_row(00000)  #00000 not a real player

def season_hitting_row2(player_id, season=2020):
    player_url = MLB_URL + f'/named.sport_hitting_tm.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id=%27{player_id}%27&season=%27{season}%27'
    resp = requests.get(player_url)
    qr = clean_json(resp)['sport_hitting_tm']['queryResults']

    if 'row' in qr:
        return Series(qr['row']).to_frame(player_id).T
    else:
        return DataFrame()

season_hitting_row2(00000)  # not a real player

season_hitting_row2(642165)  # vanmeter, traded midseason

season_hitting_data(642165)

def season_hitting_rows(player_id, season=2020):
    player_url = MLB_URL + f'/named.sport_hitting_tm.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id=%27{player_id}%27&season=%27{season}%27'
    resp = requests.get(player_url)
    qr = clean_json(resp)['sport_hitting_tm']['queryResults']

    if 'row' in qr:
        raw_data = qr['row']
        if type(raw_data) is dict:
            raw_data = [raw_data]
        return DataFrame(raw_data)
    else:
        return DataFrame()

season_hitting_rows(642165)
season_hitting_rows(605113)

hitting_2020 = pd.concat([season_hitting_rows(x) for x in
                          rosters_all.head(100).index], ignore_index=True)

# other functions
# season pitching

def qr_to_df(qr):
    if 'row' in qr:
        raw_data = qr['row']
        if type(raw_data) is dict:
            raw_data = [raw_data]
        return DataFrame(raw_data)
    else:
        return DataFrame()


def season_hitting_rows(player_id, season=2020):
    player_url = MLB_URL + f'/named.sport_hitting_tm.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id=%27{player_id}%27&season=%27{season}%27'
    resp = requests.get(player_url)
    qr = clean_json(resp)['sport_hitting_tm']['queryResults']
    return qr_to_df(qr)

def season_pitching_rows(player_id, season=2020):
    player_url = MLB_URL + f'/named.sport_pitching_tm.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id=%27{player_id}%27&season=%27{season}%27'
    resp = requests.get(player_url)
    qr = clean_json(resp)['sport_pitching_tm']['queryResults']
    return qr_to_df(qr)


# career hitting
def career_hitting_rows(player_id):
    player_url = MLB_URL + f'/named.sport_career_hitting.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id=%27{player_id}%27'
    resp = requests.get(player_url)
    qr = clean_json(resp)['sport_career_hitting']['queryResults']
    return qr_to_df(qr)

# career pitching
def career_pitching_rows(player_id):
    player_url = MLB_URL + f'/named.sport_career_pitching.bam?league_list_id=%27mlb%27&game_type=%27R%27&player_id=%27{player_id}%27'
    resp = requests.get(player_url)
    qr = clean_json(resp)['sport_career_pitching']['queryResults']
    return qr_to_df(qr)

# calling them:
hitting_2020 = pd.concat([season_hitting_rows(x) for x in
                          rosters_all.head(100).index], ignore_index=True)

pitching_2020 = pd.concat([season_pitching_rows(x) for x in
                           rosters_all.head(100).index], ignore_index=True)

hitting_career = pd.concat([career_hitting_rows(x) for x in
                            rosters_all.head(100).index], ignore_index=True)

pitching_career = pd.concat([career_pitching_rows(x) for x in
                            rosters_all.head(100).index], ignore_index=True)
