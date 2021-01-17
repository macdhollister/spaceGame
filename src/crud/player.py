import json

from sqlalchemy.orm import Session

from src import schemas
from src.models import *


def get_player(db: Session, player_id: int):
    db_player = db.query(Player).filter(Player.id == player_id).first()

    ships = []
    for ship in db_player.ships:
        ships.append(json.loads(str(ship)))

    return {
        "id": db_player.id,
        "faction": db_player.faction,
        "is_active": db_player.is_active,
        "ships": ships
    }


def get_player_by_faction(db: Session, faction: str):
    return db.query(Player).filter(Player.faction == faction).first()


def get_players(db: Session):
    return db.query(Player).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = Player(faction=player.faction)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def submit_turn(db: Session, turn: schemas.Turn):
    turn = Turn(
        faction=turn.faction,
        turn_number=turn.turn_number,
        orders=turn.orders
    )
    db.add(turn)
    db.commit()
    db.refresh(turn)
    return turn
