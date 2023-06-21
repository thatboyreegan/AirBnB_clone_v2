#!/usr/bin/python3
""" City Module for HBNB project """

from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """The city class, contains state ID and name"""

    __tablename__ = "cities"
    state_id = Column(
        String(60),
        ForeignKey("states.id", ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String(128), nullable=False)

    places = relationship(
        "Place",
        cascade="all, delete-orphan",
        passive_deletes=True,
        backref="cities"
    )
