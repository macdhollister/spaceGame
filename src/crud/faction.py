import json

from sqlalchemy.orm import Session

from src import models
from src import schemas


def get_faction(db: Session, faction_id: int):
    db_faction = db.query(models.Faction).filter(models.Faction.id == faction_id).first()

    ships = []
    for ship in db_faction.ships:
        ships.append(json.loads(str(ship)))

    return {
        "id": db_faction.id,
        "faction": db_faction.faction,
        "is_active": db_faction.is_active,
        "ships": ships
    }


def get_faction_by_name(db: Session, faction: str):
    return db.query(models.Faction).filter(models.Faction.faction == faction).first()


def get_factions(db: Session):
    return db.query(models.Faction).all()


def create_faction(db: Session, faction: schemas.FactionCreate):
    db_faction = models.Faction(faction=faction.faction)
    db.add(db_faction)
    db.commit()
    db.refresh(db_faction)
    return db_faction


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
