from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_db
from src.crud.faction import get_faction_by_name
from src.crud.ship import create_ship
from src import schemas

router = APIRouter(
    prefix="/ships"
)


@router.post("/")
def post_ship(ship: schemas.ShipCreate, db: Session = Depends(get_db)):
    db_owner = get_faction_by_name(db, ship.owner)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Faction not found")
    return create_ship(db, ship)
