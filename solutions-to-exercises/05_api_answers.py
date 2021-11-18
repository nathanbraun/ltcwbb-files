"""
Answers to the end of chapter exercise for api problems.
"""
import json
import pandas as pd
from pandas import DataFrame, Series
import requests

MLB_URL = 'http://lookup-service-prod.mlb.com/json/'

def clean_json(resp):
    return json.loads(resp.text
                      .replace('(','')
                      .replace(')','')
                      .replace(';',''))
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

player_id = 642165

season_hitting_rows(player_id)
