from typing import List

from pydantic import BaseModel

from src.schemas import Ship


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
