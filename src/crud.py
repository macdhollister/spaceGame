from sqlalchemy.orm import Session
import json

from . import models, schemas


def get_player(db: Session, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()

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
    return db.query(models.Player).filter(models.Player.faction == faction).first()


def get_players(db: Session):
    db.query(models.Player).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(faction=player.faction)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def create_ship(db: Session, ship: schemas.ShipCreate):
    db_ship = models.Ship(owner=ship.owner, modules=ship.modules)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship
