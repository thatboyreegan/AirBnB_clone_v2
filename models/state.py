#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
            "City",
            cascade="all, delete-orphan",
            passive_deletes=True,
            backref="state"
            )
    else:
        @property
        def cities(self):
            """Returns list of City instances with state_id equal to
            current State.id"""
            from models import storage
            from models.city import City

            return [
                value
                for value in storage.all(City).values()
                if value.state_id == self.id
            ]
