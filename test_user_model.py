"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

app.config['TESTING'] = True

db.drop_all()

db.create_all()

USER_1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user = USER_1
        db.session.add(user)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(USER_1.messages), 0)
        self.assertEqual(len(USER_1.followers), 0)

    def test_user_repr(self):
        '''Does the __repr__ method work?'''

        self.assertIsInstance(USER_1.id, int)
        del USER_1.id

        self.assertEqual(user, "<User #1: testuser, test@test.com>")

        # f"<User #{self.id}: {self.username}, {self.email}>"