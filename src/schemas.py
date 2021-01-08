from typing import List, Optional

from pydantic import BaseModel


# ----- PLANET -----

class Planet(BaseModel):
    id: int
    name: str
    connections: List['Planet'] = []


Planet.update_forward_refs()


# ----- SHIP -----
class Module(BaseModel):
    pass


class Ship(BaseModel):
    pass


# ----- PLAYER -----

class PlayerBase(BaseModel):
    faction: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    is_active: bool
    planets: List[Planet] = []
    ships: List[Ship] = []


# ----- FROM TUTORIAL -----

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
