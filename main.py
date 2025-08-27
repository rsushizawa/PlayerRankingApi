from fastapi import FastAPI, HTTPException
from typing import List
from model import Player, UpdatePlayer

app = FastAPI()

db: List[Player] = {
    Player(id=1,name="Donk",points=10)
}

@app.get("/players", response_model=List[Player])
def get_players():
    return db
