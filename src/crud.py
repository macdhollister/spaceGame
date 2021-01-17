from sqlalchemy.orm import Session
import json

from . import schemas
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


def create_ship(db: Session, ship: schemas.ShipCreate):
    db_ship = Ship(owner=ship.owner, modules=ship.modules)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship


def get_planets(db: Session):
    return db.query(Planet).all()


def get_planet_by_name(db: Session, planet_name: str):
    return db.query(Planet).filter(Planet.name == planet_name).first()


def create_planet(db: Session, planet: schemas.PlanetCreate):
    db_planet = Planet(name=planet.name)
    db.add(db_planet)
    db.commit()
    db.refresh(db_planet)
    return db_planet


def build_map(db: Session, planets):
    for planet in planets:
        create_planet(db, schemas.PlanetCreate.parse_obj({'name': planet['name']}))

    for planet in planets:
        db_planet = get_planet_by_name(db, planet['name'])
        for neighbor in planet['connections']:
            db_planet.make_connection(get_planet_by_name(db, neighbor))

    return get_planets(db)


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
