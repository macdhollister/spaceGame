from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()


# ----- UTILITY -----

# Dependency
def get_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        print("closing database")
        db.close()


# ----- ROUTES -----

# ----- PLAYERS -----

@app.post("/players/")
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_faction(db, faction=player.faction)
    if db_player:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_player(db=db, player=player)


@app.get("/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


# ----- SHIPS -----

@app.post("/ships/")
def create_ship(ship: schemas.ShipCreate, db: Session = Depends(get_db)):
    db_owner = crud.get_player_by_faction(db, ship.owner)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.create_ship(db, ship)
