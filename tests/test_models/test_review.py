#!/usr/bin/python3
"""Review Test module"""
import uuid
import unittest

from tests.test_models.test_base_model import test_basemodel, STORAGE_TYPE
from models.review import Review


class test_review(test_basemodel):
    """Class for testing Review"""

    def __init__(self, *args, **kwargs):
        """Initialize a new test class"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """Test place_id"""
        new = self.value()
        new.place_id = str(uuid.uuid4())
        self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """test user_id"""
        new = self.value()
        new.user_id = str(uuid.uuid4())
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """Test text"""
        new = self.value()
        new.text = "Nice"
        self.assertEqual(type(new.text), str)

    @unittest.skipUnless(STORAGE_TYPE == "db", "Testing for file storage")
    def test_save(self):
        """ Testing save """

        from tests.test_models.defaults import DefaultInstances

        DEFAULTS = DefaultInstances()

        place_id = DEFAULTS.place_id
        user_id = DEFAULTS.user_id

        i = self.value(text="Nairobi", place_id=place_id, user_id=user_id)
        i.save()
        conn = self._create_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reviews WHERE id = %s", (i.id,))
        self.assertTrue(cur.fetchone())
        cur.close()
        conn.close()
