from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_db
from src.crud.faction import get_faction_by_name, submit_turn
from .. import schemas

router = APIRouter(
    prefix="/turns"
)


@router.post("/")
def post_turn(turn: schemas.Turn, db: Session = Depends(get_db)):
    db_owner = get_faction_by_name(db, faction=turn.faction)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Faction not found")
    return submit_turn(db, turn)
    # TODO
    #   get current state of game
    #   validate turn
    #   validation fails:
    #       kick back to player
    #   validation succeeds:
    #       write to db
    #       send success message
    pass
