from sqlalchemy import Table, Boolean, Column, UniqueConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .Base import Base

connection = Table(
    'PlanetConnection', Base.metadata,
    Column('planet_a_id', Integer, ForeignKey('planets.id'), index=True),
    Column('planet_b_id', Integer, ForeignKey('planets.id')),
    UniqueConstraint('planet_a_id', 'planet_b_id', name='unique_connections')
)


class Planet(Base):
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # ships = relationship('Ship', backref="location")
    connections = relationship('Planet',
                               secondary=connection,
                               primaryjoin=id == connection.c.planet_a_id,
                               secondaryjoin=id == connection.c.planet_b_id
                               )

    def make_connection(self, other):
        if other not in self.connections:
            self.connections.append(other)
            other.connections.append(self)

    def __repr__(self):
        return '<Planet(name="%s")>' % self.name
