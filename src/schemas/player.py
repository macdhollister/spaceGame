from typing import List

from pydantic import BaseModel

from src.schemas.ship import Ship
from src.schemas.turn import Turn


class PlayerBase(BaseModel):
    faction: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    is_active: bool
    ships: List[Ship] = []
    turns: List[Turn] = []
