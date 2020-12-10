#!/usr/bin/env python

import pandas as pd

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
        pct = round(pct*100, 2)
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
        data['2P_PCT'] = round((data['2PM'] / data['2PA']), 3)

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
        team_keep_cols = ['TEAM_ABBREVIATION', 'home', 'PTS', 'FG', 'FG_PCT', '3P',\
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

    def clean_shots_df(shots_df):
        """
        This function aggregates shot dataframes to team levels and cleans it using
        function rename_cols().
        
        The output dateframe shows the shot zone area, shot zone range, number
        of shots made and attempted in each respective area. The final created
        column is the field goal percentage formatted to XX.X%.
        
        input: Concatenated player dataframe
        output: cleaned, aggregated dataframe
        """
        df = shots_df.copy()
        
        groupby_cols = ['GAME_ID', 'TEAM_NAME', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE']
        out_cols = ['GAME_ID', 'TEAM_NAME', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE',
                'SHOT_MADE_FLAG', 'SHOT_ATTEMPTED_FLAG']
        # aggregate shots
        agg_df = df.groupby(groupby_cols)[out_cols].sum().reset_index()
        # add a fg pct column and format it
        # format by leaving one decimal place and adding '%' to the end
        agg_df['rounded_fg_pct'] = round((agg_df.SHOT_MADE_FLAG / agg_df.SHOT_ATTEMPTED_FLAG)* 100).astype(int)
        agg_df['formatted_fg_pct'] = agg_df.rounded_fg_pct.apply(lambda x: str(x) + '%')
        # combine shooting fields
        df_cleaner.combine_shooting_fields(agg_df, 'SHOTS_MADE_FLAG', 'SHOTS_ATTEMPTED_FLAG', 'fg')

        # format column names
        agg_df = df_cleaner.rename_cols(agg_df)
        return agg_df

    def rename_cols(df):
        """
        This function takes an aggregated team shots dataframe and formats
        the columns to lower case. It also renames two flagged columns for
        easier readability.
        """
        data = df.copy()
        shots_cols = {
            'SHOT_MADE_FLAG' : 'shots_made',
            'SHOT_ATTEMPTED_FLAG' : 'shots_attempted'
        }
        data.rename(columns = shots_cols, inplace = True)
        # lower column names
        cols = dict()
        for col in list(data.columns):
            cols[col] = col.lower()
        data.rename(columns = cols, inplace = True)
        return data