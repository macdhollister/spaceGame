from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .Base import Base
from .Player import Player


class Turn(Base):
    __tablename__ = "turns"

    faction = Column(String, ForeignKey(Player.faction), primary_key=True)
    turn_number = Column(Integer, primary_key=True)
    orders = Column(String)

    player_relationship = relationship('Player', back_populates="turns")
