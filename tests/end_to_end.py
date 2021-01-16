import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.Base import Base
from src.routes.utils import get_db

# In memory database
DATABASE_URL = "sqlite://"


# -------------------- UTILITIES --------------------

@pytest.fixture
def client():
    # Setup database connection
    local_session = setup_database()

    # Run tests using the database previously setup
    yield TestClient(app)

    # Close the session (refreshing the database)
    local_session().close()


def setup_database():
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        Base.metadata.create_all(bind=engine)
        db = local_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return local_session


# -------------------- TESTS --------------------

def test_submit_turn(client):
    client.post("/players/", json={"faction": "faction_1"})

    response = client.post("/turns/", json={
        "faction": "faction_1",
        "turn_number": 1,
        "orders": json.dumps({
            "test": "orders_json"
        })
    })

    assert response.json() == {
        "faction": "faction_1",
        "turn_number": 1,
        "orders": '{"test": "orders_json"}'
    }


def test_create_ship(client):
    client.post("/players/", json={"faction": "faction_1"})
    response = client.post("/ships/", json={"owner": "faction_1", "modules": "D1"})

    player = client.get("/players/1")

    assert player.json() == {
        "id": 1,
        "faction": "faction_1",
        "is_active": True,
        "ships": [{"id": 1, "owner": "faction_1", "modules": "D1"}],
        "turns": []
    }

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "owner": "faction_1",
        "modules": "D1"
    }


def test_create_player(client):
    response = client.post(
        "/players/",
        json={"faction": "faction_1"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "faction": "faction_1",
        "id": 1,
        "is_active": True
    }


def test_create_two_players(client):
    response_1 = client.post(
        "/players/",
        json={"faction": "faction_1"}
    )

    response_2 = client.post(
        "/players/",
        json={"faction": "faction_2"}
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    assert response_1.json() == {
        "faction": "faction_1",
        "id": 1,
        "is_active": True
    }
    assert response_2.json() == {
        "faction": "faction_2",
        "id": 2,
        "is_active": True
    }
