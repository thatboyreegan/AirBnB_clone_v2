#!/usr/bin/python3
"""Module for testing DBStorage"""

import unittest
import MySQLdb
import os
import sqlalchemy

from models.engine.db_storage import DBStorage
from models import storage
from models.user import User
from models.state import State
from models.city import City

STORAGE_TYPE = os.environ.get("HBNB_TYPE_STORAGE")


@unittest.skipUnless(STORAGE_TYPE == "db", "Not testing database storage")
class TestDBStorage(unittest.TestCase):
    """Test DBStorage methods"""

    @staticmethod
    def __create_db_connection():
        """create a new database connection"""
        options = {
            "host": os.environ.get("HBNB_MYSQL_HOST"),
            "user": os.environ.get("HBNB_MYSQL_USER"),
            "password": os.environ.get("HBNB_MYSQL_PWD"),
            "database": os.environ.get("HBNB_MYSQL_DB"),
        }
        return MySQLdb.connect(**options)

    @staticmethod
    def __count(tablename):
        """Return the number of items in the given table

        Args:
            tablename (str): table name.
        """
        conn = TestDBStorage.__create_db_connection()
        cur = conn.cursor()
        # Using format. Not safe.
        cur.execute("""SELECT * FROM {}""".format(tablename))
        count = len(cur.fetchall())
        cur.close()
        conn.close()

        return count

    def test_storage_type(self):
        """Test that storage is an instance of DBStorage"""
        self.assertTrue(type(storage), DBStorage)

    def test_new_and_save(self):
        """Test that the new and save methods add a new object
        to the database"""

        count1 = self.__count("users")
        new_user = User(email="DBStorage", password="1234")
        storage.new(new_user)
        storage.save()
        count2 = self.__count("users")
        self.assertTrue(count2 - count1, 1)

    def test_all_without_class(self):
        """Test that the all method returns dictionary of all objects"""

        objs_dict = storage.all()
        for key, value in objs_dict.items():
            with self.subTest(key=key):
                self.assertTrue('.' in key)
                self.assertEqual(key.split('.')[0], value.__class__.__name__)
                self.assertEqual(key.split('.')[1], value.id)

    def test_all_with_class(self):
        """Test that all returns dictionary of objects in specified class"""

        for _ in range(5):
            State(name="DBStorage test all").save()

        user_objs = storage.all(User)
        for key, value in user_objs.items():
            with self.subTest(key=key):
                self.assertTrue('.' in key)
                self.assertEqual(key.split('.')[0], "User")
                self.assertEqual(key.split('.')[1], value.id)

    def test_delete(self):
        """Test that delete removes the specified object from the database"""

        new_state = State(name="DBStorage test delete")
        new_state.save()

        count1 = self.__count("states")
        storage.delete(new_state)
        storage.save()
        count2 = self.__count("states")

        self.assertEqual(count1 - count2, 1)

    def test_delete_with_not_added_obj(self):
        """Test that delete raises an exception if object is not
        persisted in the session"""

        new_state = State(name="DBStorage test delete")

        with self.assertRaises(sqlalchemy.exc.InvalidRequestError):
            storage.delete(new_state)

    def test_delete_cascades(self):
        """Test that delete does nothing if object is not specified"""

        new_state = State(name="DBStorage test delete cascade")
        new_state.save()
        City(
            name="DBStorage test delete cascade",
            state_id=new_state.id
        ).save()

        city_count1 = self.__count("cities")
        state_count1 = self.__count("states")

        storage.delete(new_state)
        storage.save()

        city_count2 = self.__count("cities")
        state_count2 = self.__count("states")

        self.assertEqual(city_count1 - city_count2, 1)
        self.assertEqual(state_count1 - state_count2, 1)
