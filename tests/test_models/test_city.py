#!/usr/bin/python3
"""City Test Module"""
import unittest

from tests.test_models.test_base_model import test_basemodel, STORAGE_TYPE
from models.city import City


class test_City(test_basemodel):
    """City test class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Test state_id"""
        new = self.value()
        new.state_id = ""
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """Test name"""
        new = self.value()
        new.name = ""
        self.assertEqual(type(new.name), str)

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_save(self):
        """ Testing save """

        from tests.test_models.defaults import DefaultInstances

        DEFAULTS = DefaultInstances()

        i = self.value(name="test", state_id=DEFAULTS.state_id)
        i.save()
        conn = self._create_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cities WHERE id = %s", (i.id,))
        self.assertTrue(cur.fetchone())
        cur.close()
        conn.close()

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_city_place_relationship(self):
        """Test that the relationship between city and place works properly"""
        from tests.test_models.defaults import DefaultInstances
        from models.place import Place

        DEFAULTS = DefaultInstances()

        new_city = self.value(name="City-Places", state_id=DEFAULTS.state_id)
        new_place = Place(
            city_id=new_city.id, user_id=DEFAULTS.user_id, name="Place-City",
            number_rooms=3, number_bathrooms=3,
            max_guest=4, price_by_night=300
        )
        new_city.save()
        new_place.save()

        self.assertTrue(new_city.places[0] is new_place)
        self.assertTrue(new_city is new_place.cities)
