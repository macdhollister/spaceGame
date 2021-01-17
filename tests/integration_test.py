import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.crud.planet import build_map
from src.models.Base import Base
from tests.fixtures import planets_without_players as planets

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
