import pytest
from fastapi.testclient import TestClient

from app.main import app, db, Player, next_id as main_next_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    global main_next_id
    db.clear()
    initial_players = [
        Player(id=4, name="Aspas", points=400),
        Player(id=3, name="Tenz", points=3000),
        Player(id=2, name="Simple", points=20000),
        Player(id=1, name="Donk", points=100000),
    ]
    db.extend(sorted(initial_players, key=lambda p: p.points))

    main_next_id = 5
    yield

# --------------------------------------------------------------------------------- eu que fiz
def test_get_players_ranking_is_descending():
    response = client.get("/players")
    assert response.status_code == 200
    data = response.json()
    
    points_list = [player["points"] for player in data]
    assert points_list == sorted(points_list, reverse=True)
    # Check the first and last players to be sure
    assert data[0]["name"] == "Donk"
    assert data[-1]["name"] == "Aspas"

def test_create_player_success():
    new_player_data = {"name": "ZywOo", "points": 50000}
    response = client.post("/create", json=new_player_data)
    
    assert response.status_code == 201
    created_player = response.json()
    assert created_player["name"] == "ZywOo"
    assert created_player["points"] == 50000
    assert created_player["id"] == 5

    # Verify the ranking is correct after insertion
    response = client.get("/players")
    data = response.json()
    assert len(data) == 5
    player_names = [p["name"] for p in data]
    assert player_names == ["Donk", "ZywOo", "Simple", "Tenz", "Aspas"]


def test_create_player_invalid_points():
    invalid_player_data = {"name": "InvalidPlayer", "points": 0}
    response = client.post("/create", json=invalid_player_data)
    assert response.status_code == 422


# <----------------------------------------------------------------------------------- IA ------------------------------------------------------------->

# --- Tests for PUT /update ---

def test_update_player_by_id_and_reorder():
    """
    Tests updating a player by ID, changing their points, and confirms
    the database list is re-sorted correctly.
    """
    update_payload = {"points": 500000}
    response = client.put("/update?player_id=4", json=update_payload) # Update Aspas (id 4)
    
    assert response.status_code == 200
    updated_player = response.json()
    assert updated_player["id"] == 4
    assert updated_player["name"] == "Aspas"
    assert updated_player["points"] == 500000
    
    # Verify the list has been re-sorted, Aspas should be at the top of the ranking
    response = client.get("/players")
    data = response.json()
    assert data[0]["name"] == "Aspas"

def test_update_player_by_name():
    """Tests successfully updating a player's name when identified by their current name."""
    update_payload = {"name": "s1mple"}
    response = client.put("/update?player_name=Simple", json=update_payload)
    
    assert response.status_code == 200
    assert response.json()["name"] == "s1mple"
    
    get_response = client.get("/players")
    player_names = [p["name"] for p in get_response.json()]
    assert "Simple" not in player_names
    assert "s1mple" in player_names

def test_update_player_not_found():
    """Tests that updating a non-existent player returns a 404 error."""
    response = client.put("/update?player_id=999", json={"name": "Ghost"})
    assert response.status_code == 404

def test_update_player_no_identifier():
    """Tests that calling update without an identifier (id or name) returns a 400 error."""
    response = client.put("/update", json={"points": 100})
    assert response.status_code == 400

# --- Tests for DELETE /delete ---

def test_delete_player_by_id():
    """Tests successfully deleting a player by ID."""
    response = client.delete("/delete?player_id=3") # Delete Tenz
    assert response.status_code == 200
    deleted_player = response.json()
    assert deleted_player["name"] == "Tenz"
    assert deleted_player["id"] == 3

    get_response = client.get("/players")
    data = get_response.json()
    assert len(data) == 3
    assert 3 not in [p["id"] for p in data]

def test_delete_player_by_name():
    """Tests successfully deleting a player by name."""
    response = client.delete("/delete?player_name=Simple")
    assert response.status_code == 200
    assert response.json()["name"] == "Simple"
    
    get_response = client.get("/players")
    player_names = [p["name"] for p in get_response.json()]
    assert "Simple" not in player_names

def test_delete_player_not_found():
    """Tests that deleting a non-existent player returns a 404 error."""
    response = client.delete("/delete?player_id=999")
    assert response.status_code == 404