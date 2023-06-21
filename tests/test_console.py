#!/usr/bin/python3
"""Module for testing the console"""

import uuid
import unittest
from io import StringIO
from unittest.mock import patch
import os
import MySQLdb

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from tests.test_models.defaults import DefaultInstances

STORAGE_TYPE = os.environ.get("HBNB_TYPE_STORAGE")


@unittest.skipIf(STORAGE_TYPE == "db", "Currently testing database storage")
class TestConsoleCreate(unittest.TestCase):
    """Class for testing the create command"""

    def test_create_with_no_arguments(self):
        """Test that create prints '** class name missing **' if called without
        any arguments"""
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create")
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class name missing **")

    def test_create_BaseModel(self):
        """Test creating new BaseModel"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f"BaseModel.{str(instance_id)}"])

    def test_create_User(self):
        """Test creating new User"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create User")
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f"User.{str(instance_id)}"])

    def test_create_Place(self):
        """Test creating new Place"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create Place")
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f"Place.{str(instance_id)}"])

    def test_create_City(self):
        """Test creating new City"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create City")
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f"City.{str(instance_id)}"])

    def test_create_Amenity(self):
        """Test creating new Amenity"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f"Amenity.{str(instance_id)}"])

    def test_create_Review(self):
        """Test creating new Review"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create Review")
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f"Review.{str(instance_id)}"])

    def test_create_State(self):
        """Test creating new State"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create State")
        instance_id = uuid.UUID(output.getvalue()[:-1])
        self.assertEqual(instance_id.version, 4)
        self.assertTrue(storage.all()[f"State.{str(instance_id)}"])

    def test_create_with_str_parameter(self):
        """Test that User instance is created with expected parameters"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create User name="Brian"')

        instance_id = uuid.UUID(output.getvalue()[:-1])
        user = storage.all()[f"User.{str(instance_id)}"]

        self.assertEqual(user.name, "Brian")
        self.assertTrue(type(user.name), str)

    def test_create_with_int_parameter(self):
        """Test that create can cast int parameter values"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create Place number_rooms=3')

        instance_id = uuid.UUID(output.getvalue()[:-1])
        place = storage.all()[f"Place.{str(instance_id)}"]

        self.assertEqual(place.number_rooms, 3)
        self.assertTrue(type(place.number_rooms), int)

    def test_create_with_float_parameter(self):
        """Test that create can cast float parameter values"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create Place latitude=33.899')

        instance_id = uuid.UUID(output.getvalue()[:-1])
        place = storage.all()[f"Place.{str(instance_id)}"]

        self.assertEqual(place.latitude, 33.899)
        self.assertTrue(type(place.latitude), float)

    def test_create_with_value_having_underscore(self):
        """Test that create correctly translates underscore to space."""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create Place name="My_place_name"')

        instance_id = uuid.UUID(output.getvalue()[:-1])
        place = storage.all()[f"Place.{str(instance_id)}"]

        self.assertEqual(place.name, "My place name")
        self.assertTrue(type(place.name), str)

    def test_create_with_multiple_parameters(self):
        """Test that create can handle different parameters."""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create User name="Kim" age=20 place_id="01"')

        instance_id = uuid.UUID(output.getvalue()[:-1])
        user = storage.all()[f"User.{str(instance_id)}"]

        self.assertEqual(user.name, "Kim")
        self.assertEqual(user.age, 20)
        self.assertEqual(user.place_id, "01")

    def test_create_parameter_without_value(self):
        """Test that passing a parameter key without a value raises no error.
        Also the key is not added to the dictionary."""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create State population')

        instance_id = uuid.UUID(output.getvalue()[:-1])
        state = storage.all()[f"State.{str(instance_id)}"]

        # Population key is not added since it has no value.
        self.assertFalse("population" in state.__dict__.keys())

    def test_create_empty_string_value(self):
        """Test that empty string is valid parameter value."""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create State name=""')

        instance_id = uuid.UUID(output.getvalue()[:-1])
        state = storage.all()[f"State.{str(instance_id)}"]

        # name is added since the empty string is a valid value.
        self.assertEqual(state.name, "")


@unittest.skipUnless(STORAGE_TYPE == "db", "Currently testing file storage")
class TestConsoleCreateDBStorage(unittest.TestCase):
    """Test the create command when using db storage"""

    def setUp(self):
        """Create defaults"""
        self.defaults = DefaultInstances()

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
        conn = TestConsoleCreateDBStorage.__create_db_connection()
        cur = conn.cursor()

        # Using format. Not safe.
        cur.execute("""SELECT * FROM {}""".format(tablename))
        count = len(cur.fetchall())
        cur.close()
        conn.close()

        return count

    def test_create_with_no_arguments(self):
        """Test that create prints '** class name missing **' if called without
        any arguments"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create")
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class name missing **")

    @unittest.expectedFailure
    def test_create_User_without_required_params(self):
        """Test creating new User"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("create User")

    def test_create_User_with_required_params(self):
        """Test creating new User"""

        count1 = self.__count("users")
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd(
                'create User email="create_user" password="1234"')

        count2 = self.__count("users")
        self.assertEqual(count2 - count1, 1)

    def test_create_State(self):
        """Test creating new State"""

        count1 = self.__count("states")
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create State name="Nairobi"')

        count2 = self.__count("states")
        self.assertEqual(count2 - count1, 1)

    def test_create_City(self):
        """Test creating new City"""

        state_id = self.defaults.state_id

        count1 = self.__count("cities")
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create City name="Meru" state_id="{}"'.
                                 format(state_id))

        count2 = self.__count("cities")
        self.assertEqual(count2 - count1, 1)

    def test_create_Place(self):
        """Test creating new Place"""

        city_id = self.defaults.city_id
        user_id = self.defaults.user_id

        count1 = self.__count("places")
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().\
                onecmd(f'create Place city_id="{city_id}"\
                       user_id="{user_id}"\
                       name="create_Place" number_rooms=12 number_bathrooms=12\
                       max_guest=6 price_by_night=100')

        count2 = self.__count("places")
        self.assertEqual(count2 - count1, 1)

    def test_create_Amenity(self):
        """Test creating new Amenity"""

        count1 = self.__count("amenities")
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd('create Amenity name="wifi"')

        count2 = self.__count("amenities")
        self.assertEqual(count2 - count1, 1)

    def test_create_Review(self):
        """Test creating new Review"""

        place_id = self.defaults.place_id
        user_id = self.defaults.user_id

        count1 = self.__count("reviews")
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd(f'create Review text="Yes"\
                                 place_id="{place_id}"\
                                user_id="{user_id}"')
        count2 = self.__count("reviews")
        self.assertEqual(count2 - count1, 1)


@unittest.skipIf(STORAGE_TYPE == "db", "Testing database storage")
class TestConsoleShow(unittest.TestCase):
    """Class for testing the show command"""

    def test_show_without_any_argument(self):
        """Test that show prints '** class name missing **' if it's called
        without any arguments"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd("show")
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class name missing **")

    def test_show_with_correct_class_and_id(self):
        """Test that show prints string representation of available instance"""

        instance = BaseModel()
        storage.new(instance)
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd(f"show BaseModel {instance.id}")
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, str(instance))

    def test_show_with_invalid_class_and_valid_id(self):
        """Test that show prints '** class doesn't exist **' if the class name
        is not found to be valid"""

        instance = BaseModel()
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd(f"show Class {instance.id}")
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** class doesn't exist **")

    def test_show_with_valid_class_and_invalid_id(self):
        """Test that show prints '** no instance found **' if the class name
        is correct but id is wrong"""

        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd(f"show BaseModel {str(uuid.uuid4())}")
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, "** no instance found **")


class TestConsoleQuit(unittest.TestCase):
    """Class for testing the quit command"""

    def test_quit(self):
        """Test that the quit command exits the interpreter"""
        with self.assertRaises(SystemExit):
            HBNBCommand().onecmd("quit")


class TestConsoleEOF(unittest.TestCase):
    """Class for testing the EOF command"""

    def test_EOF(self):
        """Test that the EOF command exits the interpreter"""
        with self.assertRaises(SystemExit):
            HBNBCommand().onecmd("EOF")


class TestConsoleHelp(unittest.TestCase):
    """Class for testing the help command"""

    def test_help_without_argument(self):
        """Test the help command without any arguments"""
        expected = """\nDocumented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update\n"""
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd(f"help")
        printed_str = output.getvalue()[:-1]
        self.assertEqual(printed_str, expected)

    def test_help_with_argument(self):
        """Test help with an argument"""
        expected = """Shows an individual instance of a class
[Usage]: show <className> <objectId>\n"""
        with patch("sys.stdout", StringIO()) as output:
            HBNBCommand().onecmd(f"help show")
        printed_str = output.getvalue()[:-1].strip(" ")
        self.assertEqual(printed_str, expected)


if __name__ == "__main__":
    unittest.main()
