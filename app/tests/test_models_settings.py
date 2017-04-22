import unittest
from peewee import *
from app import app
from ..models import db
from ..models.setting import Setting


class SettingModelTestCase(unittest.TestCase):

    def setUp(self):
        database = SqliteDatabase(":memory:")
        db.init(database)
        db.create_tables([Setting])
        db.connect()

    def tearDown(self):
        db.drop_tables([Setting], safe=True)
        db.close()

    def test_set_value_update_value(self):
        self.assertTrue(Setting.set_value('header_title', 'A new value'))

if __name__ == "__main__":
    unittest.main()
