from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .Base import Base
from .Faction import Faction


class Turn(Base):
    __tablename__ = "turns"

    faction = Column(String, ForeignKey(Faction.faction), primary_key=True)
    turn_number = Column(Integer, primary_key=True)
    initiative = Column(Integer)
    orders = Column(String)

    faction_relationship = relationship(Faction, back_populates="turns")
