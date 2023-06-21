#!/usr/bin/python3
"""Amenity Test Module"""
import unittest

from tests.test_models.test_base_model import test_basemodel, STORAGE_TYPE
from models.amenity import Amenity


class test_Amenity(test_basemodel):
    """Amenity Test Class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Test the name"""
        new = self.value()
        new.name = ""
        self.assertEqual(type(new.name), str)

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_save(self):
        """ Testing save """
        i = self.value(name="test save")
        i.save()
        conn = self._create_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM amenities WHERE id = %s", (i.id,))
        self.assertTrue(cur.fetchone())
        cur.close()
        conn.close()
