# 🏀 NBA Trade Machine & Player Impact Evaluator

A web app that evaluates hypothetical NBA trades. Pick two teams, choose the players each side is sending out, and the app returns a fairness verdict based on a machine learning impact model, an age-aware valuation, and a salary-matching check.

**Live demo:** https://nba-trade-evaluator.streamlit.app

> The API runs on a free Render instance that sleeps when idle. If the first evaluation hangs, wait up to a minute and try again.

## How it works

1. **Impact model.** A Ridge regression (scikit-learn) predicts a player's impact from per-game stats: PTS, REB, AST, STL, BLK, TOV, TS%, USG%, MIN and AGE.
2. **Age adjustment.** Each prediction is scaled by an age multiplier so that youth is rewarded and decline is penalized:
   - Under 25: `1 + 0.05 × (25 − age)` (a 19-year-old gets 1.30×)
   - 25 to 29: `1.0` (prime)
   - Over 29: `max(0.45, 1 − 0.045 × (age − 29))` (a 41-year-old gets 0.46×)
3. **Trade fairness.** Total adjusted impact is summed for each side. The fairness score is `100 − (difference ÷ higher side × 100)`:
   - 85 or above: **Fair**
   - 70 to 85: **Slightly uneven**
   - Below 70: **Unfair**
4. **CBA salary matching.** A rules module checks outgoing vs. incoming salary for each team based on its tax apron tier.

## Architecture

```
Streamlit front end (app.py)  ──HTTP──▶  FastAPI service (main.py)  ──▶  Ridge pipeline (.joblib)
        │
        └── RosterService reads nba_player_stats_with_age.csv
```

- **Front end:** Streamlit, Plotly (radar chart comparison), deployed on Streamlit Community Cloud
- **API:** FastAPI + Pydantic validation, deployed on Render. The model is trained during the build step.
- **Data:** 2025-26 per-game and advanced stats pulled with `nba_api`

## Run locally

```bash
cd nba-ml-service
pip install -r requirements.txt

# Train the model (creates nba_trade_model.joblib)
python3 train_model.py

# Terminal 1: start the API
python3 -m uvicorn main:app --reload

# Terminal 2: start the app
python3 -m streamlit run app.py
```

The app talks to `http://127.0.0.1:8000` by default. To point it at another API, set the `API_URL` environment variable (or Streamlit secret).

## Refreshing the data

`fetch_file.py` pulls stats from stats.nba.com via `nba_api` and writes the CSV. NBA's stats servers sometimes block or throttle certain networks, so run it from a different connection if it times out, then retrain with `train_model.py`.
