#!/usr/bin/python3
"""State Test module"""
import unittest
from datetime import datetime

from tests.test_models.test_base_model import test_basemodel, STORAGE_TYPE
from models.state import State


class test_state(test_basemodel):
    """Class for testing State objects"""

    def __init__(self, *args, **kwargs):
        """Initialize a test instance"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """Test name"""
        new = self.value()
        new.name = ""
        self.assertTrue(isinstance(new.name, str))

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_save(self):
        """ Testing save """
        i = self.value(name="Save")
        i.save()
        conn = self._create_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM states WHERE id = %s", (i.id,))
        self.assertTrue(cur.fetchone())
        cur.close()
        conn.close()

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_state_city_relationship(self):
        """Test that the relationship between state and cities works as
        expected"""
        from models.city import City

        new_state = self.value(name="State-Cities")
        new_city = City(name="City-State", state_id=new_state.id)
        new_state.save()
        new_city.save()

        self.assertTrue(new_city is new_state.cities[0])
        self.assertTrue(new_state is new_city.state)

    @unittest.skipIf(STORAGE_TYPE == "db", "Testing for file storage")
    def test_cities_getter(self):
        """Test that the cities getter returns a list of cities with
        state_id equal to state.id"""
        from models.city import City

        new_state = State()
        new_city = City(state_id=new_state.id,
                        created_at=datetime.now().isoformat(),
                        updated_at=datetime.now().isoformat())
        new_state.save()
        new_city.save()

        self.assertTrue(new_city is new_state.cities[0])
        with self.assertRaises(AttributeError):
            new_city.state
