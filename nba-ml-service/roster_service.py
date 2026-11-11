import os
import pandas as pd

class RosterService:
    def __init__(self, csv_path: str = "nba_player_stats_with_age.csv"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_path = os.path.join(base_dir, csv_path)
        
        self.df = pd.read_csv(resolved_path)
        self.df["AGE"] = self.df["AGE"].fillna(self.df["AGE"].median())
        self.df["name_lower"] = self.df["name"].str.lower()

    def get_teams(self):
        return sorted(self.df["team"].dropna().unique().tolist())

    def get_players_by_team(self, team_abbr: str):
        matched = self.df[self.df["team"] == team_abbr]
        return matched[["name", "team", "MIN", "PTS", "REB", "AST"]].to_dict(orient="records")

    def get_player_payload(self, player_name: str):
        match = self.df[self.df["name_lower"] == player_name.lower()]
        if match.empty:
            return None
        row = match.iloc[0]
        return {
            "name": row["name"],
            "PTS": float(row["PTS"]),
            "REB": float(row["REB"]),
            "AST": float(row["AST"]),
            "STL": float(row["STL"]),
            "BLK": float(row["BLK"]),
            "TOV": float(row["TOV"]),
            "TS_PCT": float(row["TS_PCT"]),
            "USG_PCT": float(row["USG_PCT"]),
            "MIN": float(row["MIN"]),
            "AGE": float(row["AGE"])
        }