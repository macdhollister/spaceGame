from sqlalchemy import Table, Boolean, Column, UniqueConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .Faction import Faction

from .Base import Base


class Ship(Base):
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True, index=True)
    modules = Column(String)
    owner = Column(String, ForeignKey(Faction.faction))

    owner_relationship = relationship(Faction, back_populates='ships')

    def __repr__(self):
        return f'{{"id": "{self.id}","owner": "{self.owner}","modules": "{self.modules}"}}'
