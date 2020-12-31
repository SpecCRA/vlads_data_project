#!/usr/bin/env python

import pandas as pd
from nba_api.stats.endpoints import PlayByPlayV2
from nba_api.stats.endpoints import BoxScorePlayerTrackV2

class get_rotations():
	def __init__(self):
		pass

	def get_starters(gameid):
		"""
		Gets each game's first quarter starters. 

		Returns two lists: Spurs first, opponent next
		"""
		box_score = BoxScorePlayerTrackV2(game_id=gameid).data_sets[0].get_data_frame()
		starters_df = roster_data_df[roster_data_df.START_POSITION.isin(['F', 'G', 'C'])]
		spurs_starters = list(starters_df[starters_df.TEAM_ABBREVIATION == 'SAS'].PLAYER_NAME)
		opp_starters = list(starters_df[starters_df.TEAM_ABBREVIATION != 'SAS'].PLAYER_NAME)

		return spurs_starters, opp_starters

	def get_pbp():
		pass

	def get_period_starters():
		pass