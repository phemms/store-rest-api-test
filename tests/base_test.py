"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # Make sure database exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory'
        app.config['TESTING'] = True
        with app.app_context():
            if "sqlalchemy" not in app.extensions:
                db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
