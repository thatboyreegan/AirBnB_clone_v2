#!/usr/bin/python3
"""Place test module"""
import unittest

from tests.test_models.test_base_model import test_basemodel, STORAGE_TYPE
from models.place import Place


class test_Place(test_basemodel):
    """place test class"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """Test city_id"""
        new = self.value()
        new.city_id = ""
        self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """Test user_id"""
        new = self.value()
        new.user_id = ""
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """Test name"""
        new = self.value()
        new.name = ""
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """Test description"""
        new = self.value()
        new.description = ""
        self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """Test number of rooms"""
        new = self.value()
        new.number_rooms = 3
        self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """Testing number of bathrooms"""
        new = self.value()
        new.number_bathrooms = 3
        self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """Testing max guest"""
        new = self.value()
        new.max_guest = 3
        self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """Test price by night"""
        new = self.value()
        new.price_by_night = 300
        self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """Test latitude"""
        new = self.value()
        new.latitude = 10.90
        self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """Test longitude"""
        new = self.value()
        new.longitude = 45.55
        self.assertEqual(type(new.longitude), float)

    def test_amenity_ids(self):
        """Test amenity IDs"""
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_save(self):
        """ Testing save """

        from tests.test_models.defaults import DefaultInstances

        DEFAULTS = DefaultInstances()

        i = self.value(
            city_id=DEFAULTS.city_id, user_id=DEFAULTS.user_id,
            name="Test save",
            number_rooms=3, number_bathrooms=3,
            max_guest=4, price_by_night=300
            )
        i.save()
        conn = self._create_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM places WHERE id = %s", (i.id,))
        self.assertTrue(cur.fetchone())
        cur.close()
        conn.close()

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_place_review_relationship(self):
        """Test the relationship between place and reviews works properly"""
        from tests.test_models.defaults import DefaultInstances
        from models.review import Review

        DEFAULTS = DefaultInstances()

        new_place = Place(
            city_id=DEFAULTS.city_id, user_id=DEFAULTS.user_id,
            name="Place-Review",
            number_rooms=3, number_bathrooms=3,
            max_guest=4, price_by_night=300
        )
        new_review = Review(
            user_id=DEFAULTS.user_id,
            text="Review-Place",
            place_id=new_place.id
        )
        new_place.save()
        new_review.save()

        self.assertTrue(new_place.reviews[0] is new_review)
        self.assertTrue(new_place is new_review.place)

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_place_amenity_relationship(self):
        """Test the relationship between place and amenities works properly"""
        from tests.test_models.defaults import DefaultInstances
        from models.amenity import Amenity

        DEFAULTS = DefaultInstances()

        new_place = Place(
            city_id=DEFAULTS.city_id, user_id=DEFAULTS.user_id,
            name="Place-Amenity",
            number_rooms=3, number_bathrooms=3,
            max_guest=4, price_by_night=300
        )
        new_amenity = Amenity(name="Amenity-Review")

        new_place.amenities = [new_amenity]
        new_place.save()
        new_amenity.save()

        self.assertTrue(new_place.amenities[0] is new_amenity)
        self.assertTrue(new_place is new_amenity.place_amenities[0])

        # Test that the place_amenity table was updated.
        conn = self._create_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT place_id FROM place_amenity
            WHERE amenity_id = %s""", (new_amenity.id,))
        self.assertEqual(cur.fetchone()[0], new_place.id)

        cur.close()
        conn.close()
