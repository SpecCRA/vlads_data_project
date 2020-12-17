# Update (12-16-20)
* Automation script done for everything except rotations data

# Update (12-10-20)
* Began building Python automation script
* Forgot to create 0-0 rows for parts that do not show up with league averages

# Update (11-24-20)

* Fixed shots formatting
    * rearranged separate FGM and FGA columns into FGM-FGA
    * reformatted shot percentages to XX%
    * added difference from league average to each team shots file

* Finished script to get required shot chart data
    * team shots per zone
    * shots made and attempted per zone
    * shot percentage per zone formatted in XX.X%

# Scraper outputs
The scraper will work game by game and will only save the **most recent game**.

1. Spurs' traditional player box score outputs
2. Opponent traditional player box score outputs
3. Spurs' traditional team box score outputs
4. Opponent traditional team box score outputs
5. Misc team game statistics
6. Spurs' shot data by zone
7. Opponent shot data by zone
8. League average shot data up the most current point of the season

# How to use scraper
* Download the entire repository
* Run `data_scraper/scraper.py` to gather, format, and output `JSON` files

## In progress:

* Rotation chart data
* Rotation chart bar graphs

# Data file notes:

* The test game is the final Spurs bubble game against the Jazz: https://www.nba.com/game/uta-vs-sas-0021901274/box-score#box-score
* `misc_box_stats.json` includes asts, rebs, pts in paint, fast break pts, 2nd chance pts, pts off turnovers, and bench points
* `players_spurs_box_score.json` and `players_opp_box_scores.json` are the player box scores
* `team_box_scores_x.json` are the two team box scores
* `shots_spurs.json` and `shots_opp.json` include shots data for each team by zones; includes FG made, FG attempted, and FG percentage
	* FG_DIFF is the difference between the shot area percentage and league average from that zone
	* FG_DIFF is calculated by TEAM SHOT ZONE FG PCT - LEAGUE AVG SHOT ZONE FG PCT
* `shots_league_avg.json` is the league average shot data for the 2019-20 season
	
# Follow-up notes - **VLAD, you can ignore the following**

# To-do

1. Parse rotations data into bins for visualization

# Rotations chart:

1. 30 second bins
2. solid bars for the game

# env name - nba-scraper