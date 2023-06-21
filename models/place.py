#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import os

from models.base_model import BaseModel, Base


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        ),
    )


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'

    city_id = Column(
        String(60),
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        String(60),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            cascade="all, delete-orphan",
            passive_deletes=True,
            backref="place"
        )
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities"
        )

    else:
        @property
        def reviews(self):
            """Returns the list of Review instances with place_id
            equals to the current Place.id

            Returns:
                list: List of Review instances.
            """
            from models import storage
            from models.review import Review

            return [
                review
                for review in storage.all(Review).values()
                if review.place_id == self.id
            ]

        @property
        def amenities(self):
            """Returns the list of Amenity instances with based on
            the attribute amenity_ids.

            Returns:
                list: List of Amenity instances.
            """

            from models import storage
            from models.amenity import Amenity

            return [
                amenity
                for amenity in storage.all(Amenity).values()
                if amenity.id in self.amenity_ids
            ]

        @amenities.setter
        def amenities(self, obj):
            """Appends the obj id to amenity_ids if obj is of
            class Amenity else do nothing.

            Args:
                obj (object): Object whose to append the id.
            """
            from models.amenity import Amenity

            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
