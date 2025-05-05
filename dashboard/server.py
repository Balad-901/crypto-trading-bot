# dashboard/server.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILES = {
    "decisions": "logs/decisions.json",
    "trades": "logs/trades.json",
    "sentiment": "logs/sentiment_history.json"
}

def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"message": "🚀 Trading Dashboard API is running."}

@app.get("/api/decisions")
def get_decisions():
    return load_data(DATA_FILES["decisions"])

@app.get("/api/trades")
def get_trades():
    return load_data(DATA_FILES["trades"])

@app.get("/api/sentiment")
def get_sentiment():
    return load_data(DATA_FILES["sentiment"])
