from typing import List

from pydantic import BaseModel

from src.schemas.ship import Ship
from src.schemas.turn import Turn


class FactionBase(BaseModel):
    faction: str


class FactionCreate(FactionBase):
    pass


class Faction(FactionBase):
    id: int
    is_active: bool
    ships: List[Ship] = []
    turns: List[Turn] = []
