import pandas as pd
import time
from nba_api.stats.endpoints import leaguedashplayerstats

stats = leaguedashplayerstats.LeagueDashPlayerStats(
    season='2025-26',
    per_mode_detailed='PerGame'
)

df_stats = stats.get_data_frames()[0]

time.sleep(1)

adv_stats = leaguedashplayerstats.LeagueDashPlayerStats(
    season='2025-26',
    measure_type_detailed_defense='Advanced',
    per_mode_detailed='PerGame'
)

df_adv = adv_stats.get_data_frames()[0]

df_stats_clean = df_stats[[
    'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'GP', 
    'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV'
]]

df_advstats_clean = df_adv[[
    'PLAYER_ID', 'TS_PCT', 'USG_PCT', 'OFF_RATING', 'DEF_RATING', 'NET_RATING'
]]

merged_df = pd.merge(df_stats_clean, df_advstats_clean, on='PLAYER_ID')

final_df = merged_df[(merged_df['GP'] >= 10) & (merged_df['MIN'] >= 10.0)].copy()

final_df.rename(columns={
    'PLAYER_ID': 'player_id',
    'PLAYER_NAME': 'name',
    'TEAM_ABBREVIATION': 'team',
}, inplace=True)

output_file = 'nba_player_stats.csv'
final_df.to_csv(output_file, index=False) 