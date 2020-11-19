Update (11-18-20)

* Grabbed each team's starters
* cleaned up columns to game time, period, player in, player out 
* Next up: one hot encode 30 second bins
 	* Address overlapping conflicts
 	* prelim method: give it to the player who played more minutes
 	* he is going to be the one that is most interesting to a general audience

# Scraper result

## Notes & Questions
* 11-8-20: All box score values to correct decimal points fixed

# Data file notes:

* `misc_box_stats.json` includes asts, rebs, pts in paint, fb pts, 2nd chance pts, pts off tov, and bench points
* `players_spurs_box_score.json` and `players_opp_box_scores.json` are the player box scores
* `team_box_scores_x.json` are the two team box scores
* `subs_data.json` is the scraped substitution data for now 

# For Vlad

* Can't find quarter by quarter point totals
	
# Follow-up notes on box scores - **VLAD, you can ignore the following**

# To-do

1. Parse rotations data: player time in, player time out (figure out format with Vlad first)
2. Shot chart data only needs to be in regions

# Rotations chart:

1. 30 second bins
2. solid bars for the game

# Shot charts:

1. Game by game shot charts
2. Team shot charts

# env name - nba-scraper
