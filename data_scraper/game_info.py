#!/usr/bin/env python

import pandas as pd
import time
from nba_api.stats.static.teams import find_teams_by_nickname, find_team_name_by_id
from nba_api.stats.static.players import find_players_by_full_name
from nba_api.stats.endpoints import LeagueGameFinder
from nba_api.stats.endpoints import BoxScorePlayerTrackV2

class game_info():

    def __init__(self):
        pass

    def get_spurs_id():
        """
        Generates Spurs NBA API team ID
        """
        spurs_info = find_teams_by_nickname('spurs') # find spurs nickname
        spurs_id = spurs_info[0]['id'] # get spurs team ID
        return spurs_id
    
    def get_opp_team_id(gameid):
        """
        Returns opponent's team ID
        """
        roster_data_df = BoxScorePlayerTrackV2(game_id=gameid).data_sets[0].get_data_frame()
        opp_teamid = roster_data_df[roster_data_df.TEAM_ABBREVIATION != 'SAS'].TEAM_ID.iloc[0]

        return opp_teamid

    def get_opp_team_name_abbrev(opp_id):
        opp_name = find_team_name_by_id(opp_id)
        return opp_name['abbreviation']

    def get_most_recent_game(team_id, season):
        """
        Returns most recent game ID and home status
        """
        home = None
        game_date = None
        gamefinder = LeagueGameFinder(team_id_nullable=team_id, \
                            season_nullable=season)
        spurs_games_df = gamefinder.get_data_frames()[0]
        game_id = spurs_games_df.iloc[0]['GAME_ID']
        game_date = spurs_games_df.iloc[0]['GAME_DATE']
        if '@' in spurs_games_df.iloc[0]['MATCHUP']:
            home = False
        else:
            home = True
        return game_id, home, game_date

    def get_playerid(name):
        """
        Finds a player's unique ID by his name.
        """
        return find_players_by_full_name(name)[0]['id']

    def get_players_list(gameid):
        """
        Returns a dictionary of player names to unique player IDs
        """
        player_ids = dict()

        roster_data_df = BoxScorePlayerTrackV2(game_id=gameid).data_sets[0].get_data_frame()
        for name in list(roster_data_df['PLAYER_NAME']):
            player_ids[name] = self.get_playerid(name)

        return player_ids

    def get_rosters(gameid):
        """
        Input a game ID and output both rosters in two lists
        """
        roster_data_df = BoxScorePlayerTrackV2(game_id=gameid).data_sets[0].get_data_frame()
        time.sleep(3)
        spurs_roster_list = list(roster_data_df[roster_data_df.TEAM_ABBREVIATION == 'SAS'].PLAYER_NAME)
        opp_roster_list = list(roster_data_df[roster_data_df.TEAM_ABBREVIATION != 'SAS'].PLAYER_NAME)
        return spurs_roster_list, opp_roster_list