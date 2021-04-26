"""
Answers to the end of chapter exercises for SQL chapter.

Note: this assumes you've already created/populated the SQL database as
outlined in the book and ./code/04_sql.py.
"""
import pandas as pd
from os import path
import sqlite3

DATA_DIR = '/Users/nathanbraun/fantasymath/fantasybook-baseball/data/100-game-sample'

conn = sqlite3.connect(path.join(DATA_DIR, 'baseball.sqlite'))

###############################################################################
# 4.1
###############################################################################
# a
df = pd.read_sql(
    """
    SELECT date, player_game.team, player_game.opp, batter, n_atbats, hit AS H,
           homerun AS HR
    FROM player_game, game, team
    WHERE
        player_game.g_id = game.g_id AND
        player_game.team = team.teamID AND
        team.lgID = 'AL' AND
        team.divID = 'E'
    """, conn)

# b
df = pd.read_sql(
    """
    SELECT date, pg.team, pg.opp, p.first_name, p.last_name, n_atbats,
           hit AS H, homerun AS HR
    FROM player_game As pg, game AS g, team AS t, player AS p
    WHERE
        pg.g_id = g.g_id AND
        pg.team = t.teamID AND
        p.id = pg.batter_id AND
        t.lgID = 'AL' AND
        t.divID = 'E'
    """, conn)

###############################################################################
# 4.2
###############################################################################
df = pd.read_sql(
    """
    SELECT g.*, th.name as home_full, ta.name as away_full
    FROM game AS g, team AS th, team AS ta
    WHERE
        g.home_team = th.teamID AND
        g.away_team = ta.teamID
    """, conn)
