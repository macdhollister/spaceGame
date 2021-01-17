from pydantic import BaseModel


class Turn(BaseModel):
    faction: str
    turn_number: int
    orders: str
