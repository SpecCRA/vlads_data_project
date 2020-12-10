#!/usr/bin/env python
import pandas as pd
from nba_api.stats.endpoints import BoxScoreTraditionalV2
from nba_api.stats.endpoints import BoxScoreMiscV2
import time

class get_box_scores():
    def __init__(self):
        pass

    def get_player_box_score(gameid):
        df = BoxScoreTraditionalV2(game_id=gameid).data_sets[0].get_data_frame()
        time.sleep(3)
        return df

    def get_team_box_score(gameid):
        df = BoxScoreTraditionalV2(game_id=gameid).data_sets[1].get_data_frame()
        time.sleep(3)
        return df

    def get_misc_stats(gameid):
    	df = BoxScoreMiscV2(game_id=spurs_games[0]).data_sets[1].get_data_frame()

    	time.sleep(3)
    	return df

    def get_bench_stats(gameid):
    	df = BoxScoreTraditionalV2(game_id=gameid).data_sets[2].get_data_frame()
    	time.sleep(3)
    	return df