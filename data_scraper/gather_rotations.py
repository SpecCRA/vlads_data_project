#!/usr/bin/env python

import pandas as pd
from nba_api.stats.endpoints import PlayByPlayV2
from nba_api.stats.endpoints import BoxScorePlayerTrackV2
import re
import time

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

		time.sleep(3)

		return spurs_starters, opp_starters

	def get_pbp(gameid):
		pbp_df = PlayByPlayV2(game_id=gameid).data_sets[0].get_data_frame()
		time.sleep(3)

		return pbp_df

	def get_col(home):
	    """ 
	    This function determines whether the spurs or opponent is the home team and returns the 
	    appropriate regex player set match and dataframe column.
	    
	    spurs_or_opp can be 'spurs' or 'opp'
	    """
	    spurs_col = '{}DESCRIPTION'
	    opp_col = '{}DESCRIPTION'
	    # check home or away
	    if home == True:
	    	spurs_col = spurs_col.format('HOME')
	    	opp_col = opp_col.format('VISITOR')
	    elif home == False:
	    	spurs_col = spurs_col.format('VISITOR')
	    	opp_col = opp_col.format('HOME')

	    return spurs_col, opp_col

	def get_period_starters():
		pass

	def split_player_out(play):
	    """
	    Takes in a substitution play by play line and outputs the last name of the player exiting the game.
	    """
	    split_play = play.split('FOR')
	    return split_play[1].strip() # remove all white space

	def split_player_in(play):
	    """
	    Takes in a sub play by play line and outputs the last name of the player entering the game.
	    """
	    split_play = play.split('FOR')
	    return split_play[0][4:].strip() # remove white space & 'SUB: '

	def process_subs(pbp_df, home):
		"""
		This function processes play by play dataframe to output substitutions patterns.
		"""

		# Get appropriate column for play by play data
		spurs_col, opp_col = get_rotations.get_col(home)

		# Split dataframe into spurs and opponents
		spurs_sub_df = pbp_df[
		    (pbp_df[spurs_col].notnull()) & # remove None values
		    (pbp_df[spurs_col].str.contains('SUB')) # query if it contains subs
		][['GAME_ID', 'PERIOD', 'PCTIMESTRING', spurs_col]].copy()

		opp_sub_df = pbp_df[
		    (pbp_df[opp_col].notnull()) &
		    (pbp_df[opp_col].str.contains('SUB'))
		][['GAME_ID', 'PERIOD', 'PCTIMESTRING', opp_col]].copy()

		# Assign columns for player in and out
		spurs_sub_df['player_in'] = spurs_sub_df[spurs_col].apply(get_rotations.split_player_in)
		spurs_sub_df['player_out'] = spurs_sub_df[spurs_col].apply(get_rotations.split_player_out)

		opp_sub_df['player_in'] = opp_sub_df[opp_col].apply(get_rotations.split_player_in)
		opp_sub_df['player_out'] = opp_sub_df[opp_col].apply(get_rotations.split_player_out)

		return spurs_sub_df, opp_sub_df