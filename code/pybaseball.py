import statsapi

schedule = statsapi.schedule(start_date='06/24/2017', end_date='06/27/2017')

"http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27mlb%27&active_sw=%27Y%27&name_part=%27mookie%25%27"

BASE_URL = 'https://statsapi.mlb.com/api/'

schedule = statsapi.schedule(start_date='06/24/2017', end_date='06/27/2017')

schedule = statsapi.schedule(start_date='07/04/2022', end_date='07/04/2022')

foo = statsapi.lookup_player('mookie')

start_date = '06/24/2017'
end_date = '06/27/2017'
params.update({"startDate": start_date, "endDate": end_date})

params = {}

def schedule(
    date=None,
    start_date=None,
    end_date=None,
    team="",
    opponent="",
    sportId=1,
    game_id=None,
):
    """Get list of games for a given date/range and/or team/opponent."""
    if end_date and not start_date:
        date = end_date
        end_date = None

    if start_date and not end_date:
        date = start_date
        start_date = None

    params = {}

    if date:
        params.update({"date": date})
    elif start_date and end_date:
        params.update({"startDate": start_date, "endDate": end_date})

    if team != "":
        params.update({"teamId": str(team)})

    if opponent != "":
        params.update({"opponentId": str(opponent)})

    if game_id:
        params.update({"gamePks": game_id})

    hydrate = (
        "decisions,probablePitcher(note),linescore,broadcasts,game(content(media(epg)))"
    )
    if date == "2014-03-11" or (str(start_date) <= "2014-03-11" <= str(end_date)):
        # For some reason the seriesStatus hydration throws a server error on 2014-03-11 only (checked back to 2000)
        logger.warning(
            "Excluding seriesStatus hydration because the MLB API throws an error for 2014-03-11 which is included in the requested date range."
        )
    else:
        hydrate += ",seriesStatus"
    params.update(
        {
            "sportId": str(sportId),
            "hydrate": hydrate,
        }
    )

    r = get("schedule", params)

    games = []
    if r.get("totalItems") == 0:
        return games  # TODO: ValueError('No games to parse from schedule object.') instead?
    else:
        for date in r.get("dates"):
            for game in date.get("games"):
                game_info = {
                    "game_id": game["gamePk"],
                    "game_datetime": game["gameDate"],
                    "game_date": date["date"],
                    "game_type": game["gameType"],
                    "status": game["status"]["detailedState"],
                    "away_name": game["teams"]["away"]["team"].get("name", "???"),
                    "home_name": game["teams"]["home"]["team"].get("name", "???"),
                    "away_id": game["teams"]["away"]["team"]["id"],
                    "home_id": game["teams"]["home"]["team"]["id"],
                    "doubleheader": game["doubleHeader"],
                    "game_num": game["gameNumber"],
                    "home_probable_pitcher": game["teams"]["home"]
                    .get("probablePitcher", {})
                    .get("fullName", ""),
                    "away_probable_pitcher": game["teams"]["away"]
                    .get("probablePitcher", {})
                    .get("fullName", ""),
                    "home_pitcher_note": game["teams"]["home"]
                    .get("probablePitcher", {})
                    .get("note", ""),
                    "away_pitcher_note": game["teams"]["away"]
                    .get("probablePitcher", {})
                    .get("note", ""),
                    "away_score": game["teams"]["away"].get("score", "0"),
                    "home_score": game["teams"]["home"].get("score", "0"),
                    "current_inning": game.get("linescore", {}).get(
                        "currentInning", ""
                    ),
                    "inning_state": game.get("linescore", {}).get("inningState", ""),
                    "venue_id": game.get("venue", {}).get("id"),
                    "venue_name": game.get("venue", {}).get("name"),
                    "national_broadcasts": list(
                        set(
                            broadcast["name"]
                            for broadcast in game.get("broadcasts", [])
                            if broadcast.get("isNational", False)
                        )
                    ),
                    "series_status": game.get("seriesStatus", {}).get("result"),
                }
                if game["content"].get("media", {}).get("freeGame", False):
                    game_info["national_broadcasts"].append("MLB.tv Free Game")
                if game_info["status"] in ["Final", "Game Over"]:
                    if game.get("isTie"):
                        game_info.update({"winning_team": "Tie", "losing_Team": "Tie"})
                    else:
                        game_info.update(
                            {
                                "winning_team": game["teams"]["away"]["team"].get(
                                    "name", "???"
                                )
                                if game["teams"]["away"].get("isWinner")
                                else game["teams"]["home"]["team"].get("name", "???"),
                                "losing_team": game["teams"]["home"]["team"].get(
                                    "name", "???"
                                )
                                if game["teams"]["away"].get("isWinner")
                                else game["teams"]["away"]["team"].get("name", "???"),
                                "winning_pitcher": game.get("decisions", {})
                                .get("winner", {})
                                .get("fullName", ""),
                                "losing_pitcher": game.get("decisions", {})
                                .get("loser", {})
                                .get("fullName", ""),
                                "save_pitcher": game.get("decisions", {})
                                .get("save", {})
                                .get("fullName"),
                            }
                        )
                    summary = (
                        date["date"]
                        + " - "
                        + game["teams"]["away"]["team"].get("name", "???")
                        + " ("
                        + str(game["teams"]["away"].get("score", ""))
                        + ") @ "
                        + game["teams"]["home"]["team"].get("name", "???")
                        + " ("
                        + str(game["teams"]["home"].get("score", ""))
                        + ") ("
                        + game["status"]["detailedState"]
                        + ")"
                    )
                    game_info.update({"summary": summary})
                elif game_info["status"] == "In Progress":
                    game_info.update(
                        {
                            "summary": date["date"]
                            + " - "
                            + game["teams"]["away"]["team"]["name"]
                            + " ("
                            + str(game["teams"]["away"].get("score", "0"))
                            + ") @ "
                            + game["teams"]["home"]["team"]["name"]
                            + " ("
                            + str(game["teams"]["home"].get("score", "0"))
                            + ") ("
                            + game["linescore"]["inningState"]
                            + " of the "
                            + game["linescore"]["currentInningOrdinal"]
                            + ")"
                        }
                    )
                else:
                    summary = (
                        date["date"]
                        + " - "
                        + game["teams"]["away"]["team"]["name"]
                        + " @ "
                        + game["teams"]["home"]["team"]["name"]
                        + " ("
                        + game["status"]["detailedState"]
                        + ")"
                    )
                    game_info.update({"summary": summary})

                games.append(game_info)

        return games
