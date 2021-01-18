import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.crud.planet import build_map
from src.crud.turn import get_all_turns, submit_turn
from src.crud.faction import create_faction
from src.models.Base import Base
from tests.fixtures import planets_without_factions as planets

from src import schemas

import json

# In memory database
DATABASE_URL = "sqlite://"


# -------------------- UTILITIES --------------------

@pytest.fixture
def db():
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = local_session()
    try:
        yield db
    finally:
        db.close()

    local_session().close()


# -------------------- TESTS --------------------

def test_build_map(db):
    game_map = build_map(db, planets)

    assert game_map[0].name == 'planet_a'
    assert game_map[1].name == 'planet_b'
    assert game_map[2].name == 'planet_c'

    assert game_map[1] in game_map[0].connections
    assert game_map[2] in game_map[0].connections

    assert game_map[0] in game_map[1].connections
    assert game_map[2] in game_map[1].connections

    assert game_map[0] in game_map[2].connections
    assert game_map[1] in game_map[2].connections


def test_get_turns_correct_order(db):
    create_faction(db, schemas.FactionCreate.parse_obj({'faction': 'faction_1'}))
    create_faction(db, schemas.FactionCreate.parse_obj({'faction': 'faction_2'}))

    # Turns should be returned in ascending order by turn_number
    # TODO there should be a secondary ordering by descending initiative
    #   tertiary ordering on time received
    submit_turn(db, schemas.Turn.parse_obj({
        "faction": "faction_1",
        "turn_number": 1,
        "orders": json.dumps({
            "test_orders": 1
        })
    }))

    submit_turn(db, schemas.Turn.parse_obj({
        "faction": "faction_1",
        "turn_number": 2,
        "orders": json.dumps({
            "test_orders": 2
        })
    }))

    submit_turn(db, schemas.Turn.parse_obj({
        "faction": "faction_2",
        "turn_number": 1,
        "orders": json.dumps({
            "test_orders": 3
        })
    }))

    all_turns = get_all_turns(db)

    assert all_turns[0].turn_number == 1
    assert all_turns[1].turn_number == 1
    assert all_turns[2].turn_number == 2
