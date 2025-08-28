from fastapi import FastAPI, HTTPException
from typing import List,Optional
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

def find_player_index_by_id(player_id: int) -> int:
    for i, player in enumerate(db):
        if player.id == player_id:
            return i
    raise HTTPException(status_code=404, detail=f"Player with id {player_id} not found")

def find_player_index_by_name(player_name: str) -> int:
    for i, player in enumerate(db):
        if player.name == player_name:
            return i
    raise HTTPException(status_code=404, detail=f"Player with name '{player_name}' not found")

@app.put("/update", response_model=Player)
def update_player(update_payload: UpdatePlayer, player_id: Optional[int] = None, player_name: Optional[str] = None):
    if player_id is None and player_name is None:
        raise HTTPException(status_code=400, detail="Must provide either player_id or player_name to identify the player.")
    if player_id is not None and player_name is not None:
        raise HTTPException(status_code=400, detail="Cannot provide both player_id and player_name. Please use one.")

    index = -1
    if player_id is not None:
        index = find_player_index_by_id(player_id)
    else:
        index = find_player_index_by_name(player_name)

    player_to_update = db.pop(index)

    original_data = player_to_update.model_dump()
    update_data_from_request = update_payload.model_dump(exclude_unset=True)
    original_data.update(update_data_from_request)
    updated_player = Player(**original_data)

    new_insertion_index = bisect_left(KeyWrapper(db, key=lambda p: p.points), updated_player.points)
    db.insert(new_insertion_index, updated_player)

    return updated_player


