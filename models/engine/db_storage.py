#!/usr/bin/python3
"""This module defines a class that manages database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.review import Review
from models.city import City

HBNB_ENV = os.environ.get("HBNB_ENV")
HBNB_MYSQL_USER = os.environ.get("HBNB_MYSQL_USER")
HBNB_MYSQL_PWD = os.environ.get("HBNB_MYSQL_PWD")
HBNB_MYSQL_HOST = os.environ.get("HBNB_MYSQL_HOST")
HBNB_MYSQL_DB = os.environ.get("HBNB_MYSQL_DB")


class DBStorage(object):
    """Database storage"""

    __engine = None
    __session = None

    classes = {
        "State": State,
        "City": City,
        "User": User,
        "Place": Place,
        "Amenity": Amenity,
        "Reviewer": Review
    }

    def __init__(self):
        """Instantiate a DBStorage instance"""

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB
            ),
            pool_pre_ping=True,
        )

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return all objects on current database session of class cls.
        If cls is None return all objects.

        Args:
            cls (class): Class of the objects to return. Defaults to None.
        """

        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for key in self.classes.keys():
                obj = self.__session.query(self.classes[key]).all()
                objs.extend(obj)

        objs_dict = {}
        for obj in objs:
            key = f"{obj.__class__.__name__}.{obj.id}"
            objs_dict[key] = obj
        return objs_dict

    def new(self, obj):
        """Add obj to the current database session

        Args:
            obj (object): Object to add to the session
        """

        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session if not node.

        Args:
            obj (object): Object to delete. Defaults to None.
        """

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()
