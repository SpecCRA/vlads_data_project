#!/usr/bin/env python

import pandas as pd
from nba_api.stats.endpoints import ShotChartLineupDetail
from nba_api.stats.endpoints import ShotChartDetail
from nba_api.stats.static.players import find_players_by_full_name
import time

class get_shots_data():
    def __init__(self):
        pass

    def get_playerid(name):
        """
        Inputs a player's full name and outputs his player ID
        """
        return find_players_by_full_name(name)[0]['id']

    def get_shot_chart(playerid, teamid, gameid, season):
        """
        This function takes in a player and returns his shot chart for a specific game.
        
        Inputs:
        playerid: Player's unique ID
        teamid: Associated team ID
        gameid: Specific game ID
        season: Current NBA season in XXXX-XX format
        
        Output: Entire DataFrame with shots data
        """
        # First, set a sleep timer
        
        shots_df = ShotChartDetail(
            player_id = playerid,
            season_nullable = season,
            team_id = teamid,
            game_id_nullable = gameid,
            context_measure_simple = 'FGA'
        )

        time.sleep(8)
        
        return shots_df.data_sets[0].get_data_frame()

    def gather_team_df(gameid, player_list, teamid, season):
        """
        This function grabs an entire team's shot data separated by each shot.
        It loops through a team's roster and grabs individual team's shot data.
        
        Input:
        spurs_or_opp: True or False
        gameid: unique game ID
        
        Output: concatted DataFrame of a team's game shot data
        """
        data = pd.DataFrame() # start with an empty dataframe
        for player in player_list:
            try:
                playerid = get_shots_data.get_playerid(player)
                df = get_shots_data.get_shot_chart(playerid, teamid, gameid, season)
                print('Finished gathering data for {}'.format(player))
                data = pd.concat([data, df])
            except:
                print('{} is not registered yet.'.format(player))
            
        return data

    def get_league_avg(roster, season, teamid):
        """
        This function outputs the league average shooting data up to a point in the season.

        The inputs are simply to query the API to get the second dataframe that comes with
        the endpoints.
        """
        name = get_shots_data.get_playerid(roster[0])

        league_avg = ShotChartDetail(
            season_nullable=season,
            team_id=teamid,
            player_id=name,
            context_measure_simple='FGA'
        )

        time.sleep(5)

        df = league_avg.data_sets[1].get_data_frame() # league averages is 1

        return df