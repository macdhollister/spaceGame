from sqlalchemy.orm import Session
from sqlalchemy import asc

from src import models as models
from src import schemas


def get_all_turns(db: Session):
    return db.query(models.Turn).order_by(models.Turn.turn_number.asc()).all()


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
