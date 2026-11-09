import os
from typing import List
from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "nba_trade_model.joblib")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Train the model first.")

    ml_models["pipeline"] = joblib.load(model_path)
    print("NBA Trade Evaluation Model loaded successfully.")
    yield

    ml_models.clear()

app = FastAPI(
    title="NBA Trade Evaluator ML Service",
    description="Microservice providing independent player impact ratings and trade fairness evaluations.",
    version="1.0.0",
    lifespan=lifespan
)

FEATURE_COLUMNS = [
    "PTS", "REB", "AST", "STL", "BLK", "TOV", "TS_PCT", "USG_PCT", "MIN"
]

class PlayerStats(BaseModel):
    name: str = Field(..., example="Luka Doncic")
    PTS: float = Field(..., ge=0.0, example=33.9)
    REB: float = Field(..., ge=0.0, example=9.2)
    AST: float = Field(..., ge=0.0, example=9.8)
    STL: float = Field(..., ge=0.0, example=1.4)
    BLK: float = Field(..., ge=0.0, example=0.5)
    TOV: float = Field(..., ge=0.0, example=4.0)
    TS_PCT: float = Field(..., ge=0.0, le=1.0, example=0.617)
    USG_PCT: float = Field(..., ge=0.0, le=1.00, example=0.360)
    MIN: float = Field(..., ge=0.0, le=48.0, example=37.5)

class TradeRequest(BaseModel):
    team_a_giving: List[PlayerStats] = Field(..., min_length=1)
    team_b_giving: List[PlayerStats] = Field(..., min_length=1)

class EvaluatedPlayer(BaseModel):
    name: str
    predicted_impact: float

class TradeResponse(BaseModel):
    team_a_total_impact: float
    team_b_total_impact: float
    impact_differential: float
    fairness_score: float
    verdict: str
    team_a_breakdown: List[EvaluatedPlayer]
    team_b_breakdown: List[EvaluatedPlayer]

def predict_players(players: List[PlayerStats]) -> List[EvaluatedPlayer]:
    pipeline = ml_models.get("pipeline")
    if not pipeline:
        raise HTTPException(status_code=500, detail="ML Pipeline not intialized.")

    records = [{col: getattr(p, col) for col in FEATURE_COLUMNS} for p in players]
    df = pd.DataFrame(records)

    predictions = pipeline.predict(df)

    return [
        EvaluatedPlayer(name=p.name, predicted_impact=round(float(pred), 2))
        for p, pred in zip(players, predictions)
    ]

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "nba-ml-evaluator"}

@app.post("/api/ml/evaluate-trade", response_model=TradeResponse)
def evaluate_trade(trade: TradeRequest):
    team_a_results = predict_players(trade.team_a_giving)
    team_b_results = predict_players(trade.team_b_giving)

    team_a_total = round(sum(p.predicted_impact for p in team_a_results), 2)
    team_b_total = round(sum(p.predicted_impact for p in team_b_results), 2)

    diff = round(abs(team_a_total - team_b_total), 2)
    higher_value = max(team_a_total, team_b_total)

    if higher_value <= 0:
        fairness_score = 100.0
    else:
        fairness_score = round(max(0.0, 100.0 - (diff / higher_value * 100.0)), 2)

    if fairness_score >= 85.0:
        verdict = "FAIR"
    elif fairness_score >= 70.0:
        verdict = "SLIGHTLY_UNEVEN"
    else:
        verdict = "UNFAIR"

    return TradeResponse(
        team_a_total_impact=team_a_total,
        team_b_total_impact=team_b_total,
        impact_differential=diff,
        fairness_score=fairness_score,
        verdict=verdict,
        team_a_breakdown=team_a_results,
        team_b_breakdown=team_b_results
    )