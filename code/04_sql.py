import pandas as pd
from os import path
import sqlite3

###############################################
# loading csvs and putting them in a sqlite db
###############################################

# only need to run this section once

# handle directories
DATA_DIR = '/Users/nathan/baseball-book/data'
HUNDRED_DIR = path.join(DATA_DIR, '100-game-sample')

# create connection
conn = sqlite3.connect(path.join(HUNDRED_DIR, 'baseball.sqlite'))

# load csv data
player_game = pd.read_csv(path.join(HUNDRED_DIR, 'batter-player.csv'))
player = pd.read_csv(path.join(HUNDRED_DIR, 'players.csv'))
game = pd.read_csv(path.join(HUNDRED_DIR, 'games.csv'))
team = pd.read_csv(path.join(DATA_DIR, '2018-season', 'teams.csv'))

# and write it to sql
player_game.to_sql('player_game', conn, index=False, if_exists='replace')
player.to_sql('player', conn, index=False, if_exists='replace')
game.to_sql('game', conn, index=False, if_exists='replace')
team.to_sql('team', conn, index=False, if_exists='replace')

#########
# Queries
#########
conn = sqlite3.connect(path.join(HUNDRED_DIR, 'baseball.sqlite'))

# return entire game table
df = pd.read_sql(
    """
    SELECT *
    FROM game
    """, conn)
df.head()

# return specific columns from game table + rename on the fly
df = pd.read_sql(
    """
    SELECT g_id, home_team, away_team, elapsed_time as length
    FROM game
    """, conn)
df.head()

###########
# filtering
###########

# basic filter, only rows where team is MIA
df = pd.read_sql(
    """
    SELECT g_id, home_team, away_team, elapsed_time as length
    FROM game
    WHERE venue_name = 'Oriole Park at Camden Yards'
    """, conn)
df.head()

# AND in filter
df = pd.read_sql(
    """
    SELECT g_id, home_team, away_team, elapsed_time as length
    FROM game
    WHERE venue_name = 'Oriole Park at Camden Yards' AND away_team = 'WAS'
    """, conn)
df.head()

# OR in filter
df = pd.read_sql(
    """
    SELECT g_id, home_team, away_team, elapsed_time as length
    FROM game
    WHERE home_team = 'COL' OR home_team = 'CIN'
    """, conn)
df.head()

# IN in filter
df = pd.read_sql(
    """
    SELECT g_id, home_team, away_team, elapsed_time as length
    FROM game
    WHERE home_team IN ('COL', 'CIN')
    """, conn)

# negation with NOT
df = pd.read_sql(
    """
    SELECT g_id, home_team, away_team, elapsed_time as length
    FROM game
    WHERE home_team NOT IN ('COL', 'CIN')
    """, conn)
df.head()

#########
# joining
#########

# no WHERE so fullcrossjoin
df = pd.read_sql(
    """
    SELECT
        player.first_name,
        player.last_name,
        player.team,
        team.lgID,
        team.divID
    FROM player, team
    """, conn)
df.head(10)


# add in two team columns to make clearer
df = pd.read_sql(
    """
    SELECT
        player.first_name,
        player.last_name,
        player.team as player_team,
        team.teamID as team_team,
        team.lgID,
        team.divID
    FROM player, team
    """, conn)
df.head(10)

# n of rows
df.shape

# works when we add WHERE to filter after crossjoin
df = pd.read_sql(
    """
    SELECT
        player.first_name,
        player.last_name,
        player.team,
        team.lgID,
        team.divID
    FROM player, team
    WHERE team.teamID = player.team
    """, conn)
df.head()

# add in two team columns to make clearer
df = pd.read_sql(
    """
    SELECT
        player.first_name,
        player.last_name,
        player.team as player_team,
        team.teamID as team_team,
        team.lgID,
        team.divID
    FROM player, team
    WHERE team.teamID = player.team
    """, conn)
df.head()

# adding a third table
df = pd.read_sql(
    """
    SELECT
        player.first_name,
        player.last_name,
        player.team,
        team.lgID,
        team.divID,
        player_game.*
    FROM player, team, player_game
    WHERE
        team.teamID = player.team AND
        player_game.batter_id = player.id
    """, conn)
df.head()


# adding a third table - shorthand
df = pd.read_sql(
    """
    SELECT
        p.first_name,
        p.last_name,
        p.team,
        t.lgID,
        t.divID,
        pg.*
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        t.teamID = p.team AND
        pg.batter_id = p.id
    """, conn)
df.head()

# adding an additional filter
df = pd.read_sql(
    """
    SELECT
        p.first_name,
        p.last_name,
        p.team,
        t.lgID,
        t.divID,
        pg.*
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        t.teamID = p.team AND
        pg.batter_id = p.id AND
        p.team = 'NYN'
    """, conn)
df.head()



###########
# LIMIT/TOP
###########

# SELECT *
# FROM player
# LIMIT 5

# SELECT TOP 5 *
# FROM player

df = pd.read_sql(
    """
    SELECT DISTINCT umpire_1B, umpire_2B, umpire_3B, umpire_HP
    FROM game
    """, conn)
df.head()

# UNION
# SUBQUERIES
# LEFT, RIGHT, OUTER JOINS

# SELECT *
# FROM <left_table>
# LEFT JOIN <right_table> ON <left_table>.<common_column> = <right_table>.<common_column>

df = pd.read_sql(
    """
    SELECT a.date, a.team, a.opp, a.venue_name, a.first_name, a.last_name, b.n_atbats, b.hit, b.homerun
    FROM
        (SELECT g_id, date, home_team as team, away_team as opp, id, venue_name, first_name, last_name
        FROM game, player
        WHERE
            game.home_team = player.team AND
            player.position = 'fielder'
        UNION
        SELECT g_id, date, away_team as team, home_team as opp, id, venue_name,  first_name, last_name
        FROM game, player
        WHERE
            game.away_team = player.team AND
            player.position = 'fielder') AS a
    LEFT JOIN player_game AS b ON a.g_id = b.g_id AND a.id = b.batter_id
    """, conn)

df.query("last_name == 'Acuna'")

df = pd.read_sql(
    """
    SELECT g_id, home_team as team, id, first_name, last_name
    FROM game, player
    WHERE
        game.home_team = player.team AND
        player.position = 'fielder'
    UNION
    SELECT g_id, away_team as team, id, first_name, last_name
    FROM game, player
    WHERE
        game.away_team = player.team AND
        player.position = 'fielder'
    """, conn)

