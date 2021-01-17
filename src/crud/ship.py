from sqlalchemy.orm import Session

from src import schemas
from src.models import *


def create_ship(db: Session, ship: schemas.ShipCreate):
    db_ship = Ship(owner=ship.owner, modules=ship.modules)
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship
