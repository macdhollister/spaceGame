from typing import List

from pydantic import BaseModel


# ----- SHIP -----

class ShipBase(BaseModel):
    owner: str
    modules: str


class ShipCreate(ShipBase):
    pass


class Ship(ShipBase):
    id: int


# ----- TURN -----

class Turn(BaseModel):
    faction: str
    turn_number: int
    orders: str


# ----- PLANET -----

class PlanetBase(BaseModel):
    pass


class PlanetCreate(PlanetBase):
    name: str


class Planet(PlanetBase):
    id: int
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
    ships: List[Ship] = []
    turns: List[Turn] = []
