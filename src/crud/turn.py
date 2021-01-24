import json

from math import floor
from sqlalchemy.orm import Session

from src import models as models
from src import schemas
from src.crud.faction import get_factions


def get_all_turns(db: Session):
    # TODO: This should have a secondary ordering on initiative bid
    #   and a tertiary ordering on time received
    return db.query(models.Turn).order_by(models.Turn.turn_number.asc()).all()


def get_current_turn(db: Session):
    num_factions = len(get_factions(db))
    num_turns = len(get_all_turns(db))

    return floor(num_turns/num_factions) + 1


def submit_turn(db: Session, turn: schemas.Turn):
    orders = json.loads(turn.orders)
    bid = 0
    if 'initiative_bid' in orders:
        bid = orders['initiative_bid']

    db_turn = models.Turn(
        faction=turn.faction,
        turn_number=turn.turn_number,
        initiative=bid,
        orders=turn.orders
    )
    db.add(db_turn)
    db.commit()
    db.refresh(db_turn)
    return db_turn
