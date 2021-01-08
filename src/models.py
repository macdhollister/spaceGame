from sqlalchemy import Table, Boolean, Column, UniqueConstraint, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from .database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    faction = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    # TODO
    # ships = relationship(...)
    # planets = relationship(...)


# ----- Ships -----

ship_module = Table(
    'ShipModule', Base.metadata,
    Column('ship_id', Integer, ForeignKey('ships.id'), index=True),
    Column('module_id', Integer, ForeignKey('modules.id'))
)


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)


class Ship(Base):
    __tablename__ = "ships"

    id = Column(Integer, primary_key=True, index=True)

    modules = relationship("Module", secondary=ship_module)


# ----- Planets -----

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


# todo ----- YEET DE FOLLOWING SHIT -----

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
