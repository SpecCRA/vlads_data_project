#!/usr/bin/env python

from game_info import game_info
from cleaning_functions import df_cleaner
from get_shots_data import get_shots_data
from box_scores import get_box_scores
from gather_rotations import get_rotations
import time
import os
import pandas as pd
import pprint

################
### SETUP ######
################
file_path = '../data/'

# check if a data/ folder exists
if os.path.isdir(file_path) == False:
	os.mkdir(file_path)
	print('creating data/ folder and outputting files')
else:
	print('data folder exists')

curr_season = '2020-21' # change to current season
print('Season: {}'.format(curr_season))
home = None # set true if team is at home
pp = pprint.PrettyPrinter(indent=4)

# get spurs team info
spurs_id = game_info.get_spurs_id()
time.sleep(3)
print('Spurs ID: {}'.format(spurs_id))

# get most recent game and home status
game_id, home, game_date = game_info.get_most_recent_game(spurs_id, curr_season)
time.sleep(3)
print('Game ID: {}'.format(game_id))
print('Game Date: {}'.format(game_date))
print('Home Game: {}'.format(home))

# get opp team info
opp_id = game_info.get_opp_team_id(game_id)
opp_abbrev = game_info.get_opp_team_name_abbrev(opp_id)
print('Opp: {}'.format(opp_abbrev))

# get team rosters
spurs_roster, opp_roster = game_info.get_rosters(game_id)
print('Spurs roster:')
pp.pprint(spurs_roster)
print('Opponent roster:')
pp.pprint(opp_roster)

#################################
####### TEAM BOX SCORES #########
#################################
# get box score
game_box_score_df = get_box_scores.get_team_box_score(game_id)
print('team box score retrieved')
# assign home or away
home_dict = {
	'TEAM_ABBREVIATION' : ['SAS', opp_abbrev],
	'home': [home, not home]
}
temp_df = pd.DataFrame(data=home_dict) # assign temp df to append to team df

# append temp df to home status
game_box_score_df = game_box_score_df.join(temp_df.set_index('TEAM_ABBREVIATION'), 
	on='TEAM_ABBREVIATION')

# clean and create separate team dfs
spurs_team_box_scores, opp_team_box_scores = df_cleaner.clean_team_box_score(game_box_score_df)
print('successfully cleaned team box scores')

# Output team box scores
# spurs team box score
spurs_team_box_scores.to_json(path_or_buf = file_path + '1_' + \
											'_team_box_scores_spurs.json',
								orient='records')

# opp team box score
opp_team_box_scores.to_json(path_or_buf = file_path + '2_' + \
											'_team_box_scores_opp.json',
							orient='records')

###############################
###### PLAYER BOX SCORES ######
###############################
#grab player box scores
player_box_scores_df = get_box_scores.get_player_box_score(game_id)
print('player box scores retrieved')

# clean df and separate by team
spurs_players_box_scores, opp_player_box_scores = df_cleaner.clean_player_box_score(player_box_scores_df)
print('successfully cleaned player box scores')

# Output player box scores

# spurs player box score
spurs_players_box_scores.to_json(path_or_buf = file_path + '3_' + \
												'_players_spurs_box_score.json',
									orient='records')

# opp player box score
opp_player_box_scores.to_json(path_or_buf = file_path + '4_' + \
											'_players_opp_box_score.json',
								orient='records')

#############################
### MISC TEAM DATA ##########
#############################
misc_stats_df = get_box_scores.get_misc_stats(game_id)
print('misc box scores retrieved')

# bench pts
bench_pts_df = get_box_scores.get_bench_stats(game_id)
print('bench pts retrieved')

# team ast & reb stats
team_misc_df = game_box_score_df[['GAME_ID', 'TEAM_ABBREVIATION', 'AST', 'REB']]

# clean & combine dataframes
game_misc_df = df_cleaner.clean_misc_df(misc_stats_df, bench_pts_df, team_misc_df)
print('successfully cleaned misc team box score')

# Output misc box scores
game_misc_df.to_json(path_or_buf = file_path + '5_' + '_misc_box_stats.json', 
						orient = 'records')

##############################
###### TEAM SHOTS DATA #######
##############################
# grab spurs team shots data
spurs_shots_df = get_shots_data.gather_team_df(game_id, spurs_roster, spurs_id, curr_season)
print('Spurs shot chart retrieved')

# grab opp team shots data
opp_shots_df = get_shots_data.gather_team_df(game_id, opp_roster, opp_id, curr_season)
print('opponent shot chart retrieved')

# get league averages data
league_avg_df = get_shots_data.get_league_avg(spurs_roster, curr_season, spurs_id)
print('league average shooting data retrieved')

# aggregate league averages data
league_avg_df = df_cleaner.clean_league_avg_df(league_avg_df)

# aggregate team shots df by shot zones
spurs_shots_df = df_cleaner.group_team_shots_df(spurs_shots_df)
opp_shots_df = df_cleaner.group_team_shots_df(opp_shots_df)
print('aggregated team shot charts')

# format & clean player shots data
clean_spurs_shots_df = df_cleaner.clean_team_shots_df(spurs_shots_df, league_avg_df)
clean_opp_shots_df = df_cleaner.clean_team_shots_df(opp_shots_df, league_avg_df)
print('successfully cleaned team shot dataframes')

# Output shots data
# spurs team shooting data
clean_spurs_shots_df.to_json(path_or_buf = file_path + '6_' + \
											'_shots_spurs.json',
								orient='records')

# opp team shooting data
clean_opp_shots_df.to_json(path_or_buf = file_path + '7_' + \
											'_shots_opp.json',
							orient='records')

# league averages shooting data
league_avg_df.to_json(path_or_buf = file_path + '8_' + \
										 '_shots_league_avg.json',
						orient='records')


###################################
####### ROTATIONS DATA ############
###################################
# get play by play game data
pbp_df = get_rotations.get_pbp(game_id)
print('successfully gathered play by play data')

# process pbp data
spurs_subs_df, opp_subs_df = get_rotations.process_subs(pbp_df, home)
print('successfully processed subs data')

# Output rotations into excel files
spurs_subs_df.to_excel(file_path + game_date + '_rotations_spurs.xlsx')

opp_subs_df.to_excel(file_path + game_date + '_rotations_opp.xlsx')

###################################
########### DONE! #################
###################################
print('Script finished.')