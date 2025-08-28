from fastapi import FastAPI, HTTPException
from typing import List
from model import Player, UpdatePlayer, CreatePlayer
from bisect import bisect_left

app = FastAPI()

class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key(self.it[i])

    def __len__(self):
        return len(self.it)

db: List[Player] = [
    Player(id=4,name="Aspas",points=400),
    Player(id=1,name="Donk",points=100000),
    Player(id=2,name="Simple",points=20000),
    Player(id=3,name="Tenz",points=3000),
    
]

db = sorted(db, key=lambda p: p.points)

next_id = 5

@app.get("/players", response_model=List[Player])
def get_players():
    return db

@app.post("/create", response_model=Player)
def create_player(player: CreatePlayer):
    global next_id
    new_player = Player(id=next_id, **player.model_dump())
    insertion_index = bisect_left(KeyWrapper(db, key=lambda p: p.points), new_player.points)
    db.insert(insertion_index,new_player)
    next_id += 1
    return new_player

