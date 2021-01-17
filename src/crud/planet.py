from sqlalchemy.orm import Session

from src import schemas
from src.models import *


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
