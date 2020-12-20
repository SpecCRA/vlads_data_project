#!/usr/bin/env python

import pandas as pd
import numpy as np
from functools import reduce

class df_cleaner():

    def __init__(self):
        pass

    def format_names(name):
        """
        Inputs a player's name and reformats it.

        Args:
            name ([string]): [Full player's name]
            Example: Tim Duncan

        Returns:
            [string]: [First  initial, last name]
            Example: T. Duncan
        """
        split_names = name.split(' ')
        first_name = split_names[0][0] + '.'
        split_names[0] = first_name
        return ' '.join(split_names)

    def combine_shooting_fields(df, makes_col, att_col, field_name):
        """
        This function combines the makes and attempts columns into a desired XX-XX format.
        It creates a new column that stores the information as a string.
        """
        df[field_name] = df[makes_col].astype(int).astype(str) + '-' + df[att_col].astype(int).astype(str)

    def format_pct(pct):
        """
        Takes a X.XX formatted percentage and formats it to XX%.
        It multiplies the number by 100 and rounds to the unit.
        """
        pct = round(pct*100)
        out_format = str(pct) + '%'
        return out_format

    def clean_player_box_score(df):
        """
        This cleans the player box scores into preferred formats.
        """

        # fill NA with 0
        df.fillna(0, inplace=True)  

        # convert some floats to integers to get rid of XX.0 decimal
        conv_list = list(df.columns)[9:]

        for col in conv_list:
            if 'PCT' in col:
                pass
            else:
                df[col] = df[col].astype(int)

        # combine shooting fields
        df_cleaner.combine_shooting_fields(df, 'FGM', 'FGA', 'FG')
        df_cleaner.combine_shooting_fields(df, 'FG3M', 'FG3A' , '3P')
        df_cleaner.combine_shooting_fields(df, 'FTM', 'FTA', 'FT')

        # format names
        df['name'] = df.PLAYER_NAME.apply(df_cleaner.format_names)

        # filter out columns
        player_keep_cols = ['name', 'TEAM_ABBREVIATION', 'MIN', 'PTS', 'FG',\
                            '3P', 'FT', 'AST', 'REB', 'DREB', 'OREB', 'BLK',\
                            'STL', 'TO', 'PF', 'COMMENT']

        filtered_df = df[player_keep_cols]

        spurs_player_df = filtered_df[filtered_df.TEAM_ABBREVIATION == 'SAS']
        opp_player_df = filtered_df[filtered_df.TEAM_ABBREVIATION != 'SAS']

        return spurs_player_df, opp_player_df

    def clean_team_box_score(df):
        data = df.copy()

        # create 2PM, 2PA, 2PCT columns
        data['2PM'] = data['FGM'] - data['FG3M']
        data['2PA'] = data['FGA'] - data['FG3A']
        data['2P_PCT'] = round((data['2PM'] / data['2PA']))

        # combine shooting fields
        df_cleaner.combine_shooting_fields(data, 'FGM', 'FGA', 'FG')
        df_cleaner.combine_shooting_fields(data, 'FG3M', 'FG3A', '3P')
        df_cleaner.combine_shooting_fields(data, 'FTM', 'FTA', 'FT')
        df_cleaner.combine_shooting_fields(data, '2PM', '2PA', '2P')

        # format percentages
        data['2P_PCT'] = data['2P_PCT'].apply(df_cleaner.format_pct)
        data['FG3_PCT'] = data['FG3_PCT'].apply(df_cleaner.format_pct)
        data['FG_PCT'] = data['FG_PCT'].apply(df_cleaner.format_pct)
        data['FT_PCT'] = data['FT_PCT'].apply(df_cleaner.format_pct)

        # filter out columns
        team_keep_cols = ['TEAM_ABBREVIATION', 'home', 'PTS', 'FG', 'FG_PCT','2P', '3P',\
                            'FG3_PCT', 'FT', 'FT_PCT', 'AST', 'REB', 'DREB', 'OREB',\
                            'BLK', 'STL', 'TO', 'PF']

        team_df = data[team_keep_cols]

        spurs_df = team_df[team_df['TEAM_ABBREVIATION'] == 'SAS']
        opp_df = team_df[team_df['TEAM_ABBREVIATION'] != 'SAS']

        return spurs_df, opp_df

    def clean_misc_df(misc_df, bench_df, team_df):
        """
        Gathers, cleans, and formats misc game data.
        Outputs a dataframe with a team's following statistics;
        1. game ID
        2. team abbreviation
        3. points in the paint
        4. 2nd chance points
        5. fast break points
        6. points off turnovers
        7. assists
        8. rebounds
        9. bench points
        """
        # filter bench columns
        bench = bench_df[bench_df['STARTERS_BENCH'] ==  'Bench'][['GAME_ID', 'TEAM_ABBREVIATION', 'PTS']]

        # filter misc columns
        misc_df = misc_df[['GAME_ID', 'TEAM_ABBREVIATION', 'PTS_PAINT', 'PTS_2ND_CHANCE',\
                'PTS_FB', 'PTS_OFF_TOV']]

        # filter team columns
        team_box_df = team_df[['GAME_ID', 'TEAM_ABBREVIATION', 'AST', 'REB']]

        # combine dataframes
        dfs = [bench, misc_df, team_box_df]

        out_df = reduce(lambda left, right: 
            pd.merge(left, right, on=['GAME_ID', 'TEAM_ABBREVIATION'],
                how = 'left'), dfs)

        # format columns as int
        for col in list(out_df.columns[2:]):
            out_df[col] = out_df[col].astype(int)

        # rename pts as bench points
        out_df.rename(columns={'PTS':'bench_pts'}, inplace=True)

        return out_df

    def group_team_shots_df(shots_df):
        """
        This function aggregates shot dataframes to team levels and cleans it using
        function rename_cols().
        
        The output dateframe aggregates player shots into team shots by shot zones.
        
        input: Concatenated player dataframe
        output: aggregated dataframe
        """
        df = shots_df.copy()
        
        groupby_cols = ['GAME_ID', 'TEAM_NAME', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE']
        out_cols = ['GAME_ID', 'TEAM_NAME', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE',
                'SHOT_MADE_FLAG', 'SHOT_ATTEMPTED_FLAG']
        # aggregate and sum shots
        agg_df = df.groupby(groupby_cols)[out_cols].sum().reset_index()

        return agg_df

    def clean_league_avg_df(league_avg_df):
        """
        Inputs the league average shots data and outputs a dataframe aggregated
        by the shot zone area and shot zone range.

        Shot zone area examples: left side, right side, center
        shot zone range examples: 24+ ft, 8-16 ft
        """
        groupby_cols = ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE']
        out_cols = ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'FGA', 'FGM']

        df = league_avg_df.groupby(groupby_cols)[out_cols].sum().reset_index()

        df['AVG_FG_PCT'] = round( (df['FGM'] / df['FGA']), 3)

        df['AVG_FG_PCT'] = df['AVG_FG_PCT'].apply(lambda x: round(x*100))
        df['FORMATTED_FG_PCT'] = df['AVG_FG_PCT'].apply(lambda x: str(x) + '%')

        # sort shot zone columns
        df.sort_values(by=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'], inplace=True)

        return df

    def calc_fg_pct_diff(clean_league_avg_df, shots_df):
        """
        Takes in two dataframes: 
        1. cleaned league average dataframe grouped by shot zone area & range
        2. cleaned up team shots dataframe with same grouping

        Outputs a dataframe that calculates field goal difference:
        team fg percentage by shot zone area & range versus the league average
        """

        # create league avg df with zones
        df = pd.DataFrame()
        avg_df_cols = ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'AVG_FG_PCT']
        shots_df_cols = ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'ROUNDED_FG_PCT']

        filtered_league_avg_df = clean_league_avg_df[avg_df_cols].copy()
        filtered_shots_df = shots_df[shots_df_cols].copy()
        df = filtered_league_avg_df.merge(filtered_shots_df, on = avg_df_cols[:2])

        # subtract cols
        df['FG_DIFF'] = df['ROUNDED_FG_PCT'] - df['AVG_FG_PCT']

        # return new shots df
        return df


    def clean_team_shots_df(shots_df, clean_league_avg_df):
        """
        Cleans team shot dataframes to desired formatting

        1. Create all shot zone areas and ranges based on what NBA saves
        2. Make sure there is a 0-0 for areas that are unaccounted for in a game
        3. Reformat some columns from a float to a an integer to remove XX.X decimal
        4. Create FG PCT column
        5. Format field goal percentages
        6. Format field goals to FGM-FGA
        7. Append the FG PCT difference from league average
        8. Filter columns

        Outputs cleaned and formatted data
        """

        df = shots_df.copy()

        # account for all shooting zones
        shot_zones = ['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE']
        zones = clean_league_avg_df[shot_zones].copy()
        df = zones.merge(shots_df, on = shot_zones, how='left')

        # fill in 0 for NaN values generated upon merge
        df.fillna(0, inplace=True)

        # calculate fg pct column
        df['ROUNDED_FG_PCT'] = round((df.SHOT_MADE_FLAG / df.SHOT_ATTEMPTED_FLAG)* 100)
        # address 0/0 columns
        df['ROUNDED_FG_PCT'].replace([np.inf, -np.inf, np.nan], 0, inplace=True)
        df['ROUNDED_FG_PCT'].astype(int)

        # change shot dtypes to int instead of float
        shots_cols = list(df.iloc[:, 4:7])
        for col in shots_cols:
            df[col] = df[col].astype(int)

        # format fg_pct
        df['FORMATTED_FG_PCT'] = df['ROUNDED_FG_PCT'].apply(lambda x: str(x) + '%')

        # format shooting fields
        df_cleaner.combine_shooting_fields(df, 'SHOT_MADE_FLAG', 'SHOT_ATTEMPTED_FLAG', 'FG')

        # create fg pct diff column
        diff_df = df_cleaner.calc_fg_pct_diff(clean_league_avg_df, df)
        diff_df = diff_df[['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'FG_DIFF']]
        df = df.merge(diff_df, on=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'])

        # format FG diff
        df['FORMATTED_FG_DIFF'] = df['FG_DIFF'].apply(lambda x: str(x) + '%')

        # sort shot zone columns
        df.sort_values(by=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'], inplace=True)

        # remove backcourt shots
        df = df[df['SHOT_ZONE_AREA'] != 'Back Court(BC)']


        # filter new df by shot zones and ranges with rounded fg pct
        keep_cols = ['GAME_ID', 'TEAM_NAME', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', \
                        'FG', 'FORMATTED_FG_PCT', 'FORMATTED_FG_DIFF']

        out_df = df[keep_cols]

        return out_df