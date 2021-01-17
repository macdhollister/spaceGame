from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_db
from src.crud.player import get_player_by_faction
from src.crud.ship import create_ship
from .. import schemas

router = APIRouter(
    prefix="/ships"
)


@router.post("/")
def post_ship(ship: schemas.ShipCreate, db: Session = Depends(get_db)):
    db_owner = get_player_by_faction(db, ship.owner)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return create_ship(db, ship)
