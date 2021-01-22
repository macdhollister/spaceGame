from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import schemas
from src.crud.faction import get_faction_by_name
from src.crud.turn import submit_turn
from src.crud.turn import get_current_turn
from .utils import get_db

router = APIRouter(
    prefix="/turns"
)


@router.post("/")
def post_turn(turn: schemas.Turn, db: Session = Depends(get_db)):
    # TODO faction and turn number should be determined by logged-in user and shouldn't be in the request
    db_owner = get_faction_by_name(db, faction=turn.faction)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Faction not found")

    # Get state of game
    # TODO

    # Validate orders based on state
    errors = validate_turn(db, None, turn)

    if errors:
        return JSONResponse(content={
            "errors": errors
        })

    # Save orders to db
    return submit_turn(db, turn)


def validate_turn(db, game_state, turn):
    errors = []

    current_turn = get_current_turn(db)
    if turn.turn_number != current_turn:
        errors.append("You may not submit a turn until all players have submitted.")

    return errors
