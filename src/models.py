from sqlalchemy import Table, Boolean, Column, UniqueConstraint, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from .database import Base

import enum


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    faction = Column(String, unique=True, index=True)

    # TODO
    # ships = relationship(...)
    # planets = relationship(...)


# ----- Ships -----

ship_module = Table(
    'ShipModule', Base.metadata,
    Column('ship_id', Integer, ForeignKey('ships.id'), index=True),
    Column('module_id', Integer, ForeignKey('modules.id'))
)


class ModuleType:
    def __init__(self, designation, tech_level):
        self.designation = designation
        self.tech_level = tech_level


class ModuleEnum(enum.Enum):
    # HEAVY WEAPONS
    W1 = ModuleType('W', 1)
    W2 = ModuleType('W', 2)
    W3 = ModuleType('W', 3)
    W4 = ModuleType('W', 4)
    W5 = ModuleType('W', 5)
    W6 = ModuleType('W', 6)
    W7 = ModuleType('W', 7)
    W8 = ModuleType('W', 8)
    W9 = ModuleType('W', 9)

    # POINT DEFENSE
    P1 = ModuleType('P', 1)
    P2 = ModuleType('P', 2)
    P3 = ModuleType('P', 3)
    P4 = ModuleType('P', 4)
    P5 = ModuleType('P', 5)
    P6 = ModuleType('P', 6)
    P7 = ModuleType('P', 7)
    P8 = ModuleType('P', 8)
    P9 = ModuleType('P', 9)

    # ARMOR PLATING
    A1 = ModuleType('A', 1)
    A2 = ModuleType('A', 2)
    A3 = ModuleType('A', 3)
    A4 = ModuleType('A', 4)
    A5 = ModuleType('A', 5)
    A6 = ModuleType('A', 6)
    A7 = ModuleType('A', 7)
    A8 = ModuleType('A', 8)
    A9 = ModuleType('A', 9)

    # SENSOR ARRAY
    S1 = ModuleType('S', 1)
    S2 = ModuleType('S', 2)
    S3 = ModuleType('S', 3)
    S4 = ModuleType('S', 4)
    S5 = ModuleType('S', 5)
    S6 = ModuleType('S', 6)
    S7 = ModuleType('S', 7)
    S8 = ModuleType('S', 8)
    S9 = ModuleType('S', 9)

    # ECM SUITE
    C1 = ModuleType('C', 1)
    C2 = ModuleType('C', 2)
    C3 = ModuleType('C', 3)
    C4 = ModuleType('C', 4)
    C5 = ModuleType('C', 5)
    C6 = ModuleType('C', 6)
    C7 = ModuleType('C', 7)
    C8 = ModuleType('C', 8)
    C9 = ModuleType('C', 9)

    # HANGAR BAY
    H1 = ModuleType('H', 1)
    H2 = ModuleType('H', 2)
    H3 = ModuleType('H', 3)
    H4 = ModuleType('H', 4)
    H5 = ModuleType('H', 5)
    H6 = ModuleType('H', 6)
    H7 = ModuleType('H', 7)
    H8 = ModuleType('H', 8)
    H9 = ModuleType('H', 9)

    # COMMAND BRIDGE
    B1 = ModuleType('B', 1)
    B2 = ModuleType('B', 2)
    B3 = ModuleType('B', 3)
    B4 = ModuleType('B', 4)
    B5 = ModuleType('B', 5)
    B6 = ModuleType('B', 6)
    B7 = ModuleType('B', 7)
    B8 = ModuleType('B', 8)
    B9 = ModuleType('B', 9)

    # WARP DRIVE
    D1 = ModuleType('D', 1)
    D2 = ModuleType('D', 2)
    D3 = ModuleType('D', 3)
    D4 = ModuleType('D', 4)
    D5 = ModuleType('D', 5)
    D6 = ModuleType('D', 6)
    D7 = ModuleType('D', 7)
    D8 = ModuleType('D', 8)
    D9 = ModuleType('D', 9)

    # MARINE BARRACKS
    M1 = ModuleType('M', 1)
    M2 = ModuleType('M', 2)
    M3 = ModuleType('M', 3)
    M4 = ModuleType('M', 4)
    M5 = ModuleType('M', 5)
    M6 = ModuleType('M', 6)
    M7 = ModuleType('M', 7)
    M8 = ModuleType('M', 8)
    M9 = ModuleType('M', 9)


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    type = Column('type', Enum(ModuleEnum))


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
