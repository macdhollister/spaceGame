from sqlalchemy import Table, Boolean, Column, UniqueConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .Base import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    faction = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    ships = relationship('Ship', back_populates="owner_relationship")
    # planets = relationship("Planet", backref="owner")
