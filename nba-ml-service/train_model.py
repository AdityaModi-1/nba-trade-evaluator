import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

df = pd.read_csv('nba_player_stats.csv')

raw_impact = (
    (df['PTS'] * 1.0) +
    (df['REB'] * 1.2) +
    (df['AST'] * 1.5) +
    (df['BLK'] * 2.0) +
    (df['STL'] * 2.0) -
    (df['TOV'] * 1.5) +
    (df['NET_RATING'] * 0.5) +
    (df['TS_PCT'] * 10.0)
)

df['target_impact'] = raw_impact * (df['MIN'] / 36)

feature_cols = [
    "PTS",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "TS_PCT",
    "USG_PCT",
    "MIN"
]

X = df[feature_cols]
y = df["target_impact"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("regressor", Ridge(alpha=1.0))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
print(f"R^2 Score: {r2_score(y_test, y_pred):.4f}")
print(f"Mean Squared Error (MSE): {mean_squared_error(y_test, y_pred):.4f}")

output_model_path = "nba_trade_model.joblib"
joblib.dump(pipeline, output_model_path)
print(f"Pipeline successfully serialized to '{output_model_path}'!")