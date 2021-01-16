from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_db
from .. import crud
from .. import schemas

router = APIRouter(
    prefix="/ships"
)


@router.post("/")
def create_ship(ship: schemas.ShipCreate, db: Session = Depends(get_db)):
    db_owner = crud.get_player_by_faction(db, ship.owner)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.create_ship(db, ship)
