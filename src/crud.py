from sqlalchemy.orm import Session
import json

from . import schemas
from src.models.Player import Player
from src.models.Ship import Ship
from src.models.Planet import Planet


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
    db.query(Player).all()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = Player(faction=player.faction)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def create_ship(db: Session, ship: schemas.ShipCreate):
    db_ship = Ship(owner=ship.owner, modules=ship.modules)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship
