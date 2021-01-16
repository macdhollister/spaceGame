from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_db
from .. import crud
from .. import schemas

router = APIRouter(
    prefix="/players"
)


@router.post("/")
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_faction(db, faction=player.faction)
    if db_player:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_player(db=db, player=player)


@router.get("/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player
