from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_db
from .. import crud
from .. import schemas

router = APIRouter(
    prefix="/turns"
)


@router.post("/")
def submit_turn(turn: schemas.Turn, db: Session = Depends(get_db)):
    db_owner = crud.get_player_by_faction(db, faction=turn.faction)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.submit_turn(db, turn)
    # TODO
    #   get current state of game
    #   validate turn
    #   validation fails:
    #       kick back to player
    #   validation succeeds:
    #       write to db
    #       send success message
    pass
