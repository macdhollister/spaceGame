from typing import List, Optional

from pydantic import BaseModel


# ----- SHIP -----

class ShipBase(BaseModel):
    owner: str
    modules: str


class ShipCreate(ShipBase):
    pass


class Ship(ShipBase):
    id: int


# ----- PLANET -----

class Planet(BaseModel):
    id: int
    name: str
    connections: List['Planet'] = []
    ships: List[Ship] = []


# Update forward refs to allow Planet class to self reference
Planet.update_forward_refs()


# ----- PLAYER -----

class PlayerBase(BaseModel):
    faction: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    is_active: bool
    # planets: List[Planet] = []
    ships: List[Ship] = []
