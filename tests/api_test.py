import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.main import app, get_db

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
