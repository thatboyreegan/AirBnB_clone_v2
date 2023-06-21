#!/usr/bin/python3
"""BaseModel Test Module"""
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os
import MySQLdb

STORAGE_TYPE = os.environ.get("HBNB_TYPE_STORAGE")


class test_basemodel(unittest.TestCase):
    """BaseModel test class."""

    def __init__(self, *args, **kwargs):
        """Initialize test_basemodel"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

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

    def tearDown(self):
        """Remove file"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default(self):
        """Test type of instance"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test initialization with kwargs"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test that an int key raises error"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(STORAGE_TYPE == "db", "Testing for database storage")
    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Test the str method"""
        i = self.value()
        i_dict = i.__dict__.copy()
        if "_sa_instance_state" in i_dict.keys():
            del i_dict["_sa_instance_state"]
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i_dict))

    def test_todict(self):
        """test the to_dict method"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """Test kwargs key: value is None"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        """Test id"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Test created_at"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """Test updated_at"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    @unittest.skipIf(STORAGE_TYPE == "db", "Testing for file storage")
    def test_delete_method(self):
        """Test delete method"""

        new = self.value()
        new.save()
        key = self.name + "." + new.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], new.to_dict())

        new.delete()
        with open('file.json', 'r') as f:
            j = json.load(f)
            with self.assertRaises(KeyError):
                j[key]
