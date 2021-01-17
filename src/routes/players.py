from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_db
from src.crud.player import get_player_by_faction, create_player, get_player
from .. import schemas

router = APIRouter(
    prefix="/players"
)


@router.post("/")
def post_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = get_player_by_faction(db, faction=player.faction)
    if db_player:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_player(db=db, player=player)


@router.get("/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player
