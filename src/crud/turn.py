from math import floor
from sqlalchemy.orm import Session

from src import models as models
from src import schemas
from src.crud.faction import get_factions


def get_all_turns(db: Session):
    return db.query(models.Turn).order_by(models.Turn.turn_number.asc()).all()


def get_current_turn(db: Session):
    num_factions = len(get_factions(db))
    num_turns = len(get_all_turns(db))

    return floor(num_turns/num_factions) + 1


def submit_turn(db: Session, turn: schemas.Turn):
    turn = models.Turn(
        faction=turn.faction,
        turn_number=turn.turn_number,
        orders=turn.orders
    )
    db.add(turn)
    db.commit()
    db.refresh(turn)
    return turn
