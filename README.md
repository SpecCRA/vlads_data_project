# Update (12-31-20)
* Included a substitutions scraper script
* Rotations are outputting into Excel tables
* Upon running script, rookies are still not yet registered. **SHOTS DATA ARE STILL NOT AUTOMATED.**
* Added dates to file names to avoid overwriting files every time.

# Update (12-20-20)
* Reformatted percentage rounding in team box scores to integer values instead of a single decimal float
* Data files are not up to date with last minor change, but everything else should be the same

# Update (12-18-20)
* Fixed team box scores to include 2-pointers field
* Removed back court shots from team shots data
* Included function to sort shot zones in team shots data

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

1. Spurs' traditional player box score outputs - `[date]_players_spurs_box_score.json`
2. Opponent traditional player box score outputs - `[date]_players_opp_box_scores.json`
3. Spurs' traditional team box score outputs - `[date]_team_box_scores_spurs.json`
4. Opponent traditional team box score outputs - `[date]_team_box_scores_opp.json`
5. Misc team game statistics - `[date]_misc_box_stats.json`
6. Spurs' shot data by zone - `[date]_shots_spurs.json`
7. Opponent shot data by zone - `[date]_shots_opp.json`
8. League average shot data up the most current point of the season - `[date]_shots_league_avg.json`
9. Spurs game substitutions - `[date]_rotations_spurs.xlsx`
10. Opponent game substitutions - `[date]_rotations_opp.xlsx`

# How to use scraper
* Download the entire repository
* Run `data_scraper/scraper_script.py` to gather, format, and output `JSON` files

# Warnings
* If a previous file exists, this script will overwrite the last file.
* The folder creation may not work on Windows because of the path naming notation.
	* If this is a problem, create a `data/` folder outside the scraper scripts folder.
* As of `Dec 23, 2020`, the shot chats are inaccurate because rookie players are not yet registered.

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