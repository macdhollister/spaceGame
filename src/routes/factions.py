from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .utils import get_db
from src.crud.faction import get_faction_by_name, create_faction, get_faction
from .. import schemas

router = APIRouter(
    prefix="/factions"
)


@router.post("/")
def post_faction(faction: schemas.FactionCreate, db: Session = Depends(get_db)):
    db_faction = get_faction_by_name(db, faction=faction.faction)
    if db_faction:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_faction(db=db, faction=faction)


@router.get("/{faction_id}", response_model=schemas.Faction)
def read_faction(faction_id: int, db: Session = Depends(get_db)):
    db_faction = get_faction(db, faction_id=faction_id)
    if db_faction is None:
        raise HTTPException(status_code=404, detail="Faction not found")
    return db_faction
