#!/usr/bin/python3
"""Implementation of the DefaultInstances Class"""

import MySQLdb
import os
from datetime import datetime
from typing import Any


class DefaultInstances(object):
    """Default instances for the user, state, city and place objects.

    Only single instances are created for every test. Calling the this
    class multiple times will yield the same instances.

    Their ids can be obtained to be used as foreign keys in the database.
    The ids are obtained from the following getters:
        - user => DefaultInstances.user_id
        - state => DefaultInstances.state_id
        - city => DefaultInstances.city_id
        - place => DefaultInstances.place_id

    The values of the ids as returned by this class are:
        - user_id -> "user-1"
        - state_id -> "state-1"
        - city_id -> "city-1"
        - place_id -> "place-1"

    This class is used during testing of the DBStorage.
    """
    class __DefaultInstance:
        """Class representing default instances used as
        foreign key instances"""

        def __init__(self):
            self.user_id = None
            self.state_id = None
            self.city_id = None
            self.place_id = None

        @staticmethod
        def _create_db_connection():
            """create a new database connection"""
            options = {
                "host": os.environ.get("HBNB_MYSQL_HOST"),
                "user": os.environ.get("HBNB_MYSQL_USER"),
                "password": os.environ.get("HBNB_MYSQL_PWD"),
                "database": os.environ.get("HBNB_MYSQL_DB"),
            }
            return MySQLdb.connect(**options)

        @property
        def user_id(self):
            """Create default objects for classes with ids
            used as foreign keys"""
            return self.__user_id

        @user_id.setter
        def user_id(self, value):
            """Set the user_id"""

            conn = self._create_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (id, email, password, created_at, updated_at)
                VALUES ("user-1", "DEFAULT", "DEFAULT", %s, %s)""",
                        (datetime.now(), datetime.now()))
            conn.commit()
            cur.close()
            conn.close()
            self.__user_id = "user-1"

        @property
        def state_id(self):
            """Return the state_id"""
            return self.__state_id

        @state_id.setter
        def state_id(self, value):
            """Set the state_id"""

            conn = self._create_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO states (id, name, created_at, updated_at)
                VALUES ("state-1", "DEFAULT", %s, %s)""",
                        (datetime.now(), datetime.now()))
            conn.commit()
            cur.close()
            conn.close()
            self.__state_id = "state-1"

        @property
        def city_id(self):
            """Return the city_id"""
            return self.__city_id

        @city_id.setter
        def city_id(self, value):
            """Set the city_id"""

            conn = self._create_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO cities (id, state_id, name, created_at, updated_at)
                VALUES ("city-1", "state-1", "DEFAULT", %s, %s)""",
                        (datetime.now(), datetime.now()))
            conn.commit()
            cur.close()
            conn.close()
            self.__city_id = "city-1"

        @property
        def place_id(self):
            """Return the place_id"""
            return self.__place_id

        @place_id.setter
        def place_id(self, value):
            """Set the place_id"""

            conn = self._create_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO places (id, user_id, city_id, name, number_rooms,
                    number_bathrooms, max_guest, price_by_night, created_at,
                    updated_at)
                VALUES ("place-1", "user-1", "city-1", "DEFAULT", "3", "3",
                    "4", "200", %s, %s)""",
                        (datetime.now(), datetime.now()))
            conn.commit()
            cur.close()
            conn.close()
            self.__place_id = "place-1"

    instance = None

    def __new__(cls):
        """Create a new instance"""
        if not cls.instance:
            cls.instance = cls.__DefaultInstance()

        return cls.instance

    def __getattr__(self, __name: str) -> Any:
        """Get a attribute.

        Args:
            __name (str): name of the attribute.

        Returns:
            Any: value of the attribute.
        """
        return getattr(self.instance, __name)

    def __setattr__(self, __name: str, value: Any):
        """Set an attribute.

        Args:
            __name (str): name of the attribute.
            value (Any): value of the attribute.
        """
        return setattr(self.instance, __name, value)
