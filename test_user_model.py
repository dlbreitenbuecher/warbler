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


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            location="SF"
        )
        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1",
            location="NY"
        )
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD1",
            location="NY"
        )
        db.session.add(user)
        db.session.commit()
        db.session.add(user1)
        db.session.commit()
        db.session.add(user2)
        db.session.commit()

        self.user = user
        self.user1 = user1
        self.user2 = user2
        self.client = app.test_client()

        self.user1.followers.append(self.user)
        #make file to test user model, test likes.py
        #make helper functions
        #setup follows - add instances of follows and users.follower and call
        # helper function in test


    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.user.messages), 0)
        self.assertEqual(len(self.user.followers), 0)
        self.assertEqual(self.user.location, "SF")
        self.assertNotEqual(self.user1.location, "SF")


    def test_user_repr(self):
        '''Does the __repr__ method work?'''

        self.assertNotEqual(repr(self.user), f"<User #{self.user1.id}: {self.user1.username}, {self.user.email}>")
        self.assertEqual(repr(self.user), f"<User #{self.user.id}: {self.user.username}, {self.user.email}>")

    def test_is_following(self):
        """Does _is_following method work?"""
        # is_following(self, other_user):

        self.assertTrue(User.is_following(self.user, self.user1))
        self.assertFalse(User.is_following(self.user1, self.user))
        self.assertFalse(User.is_following(self.user, self.user2))

    def test_is_followed_by(self):  
        """Does is_followed_by method work?"""  

        self.assertTrue(User.is_followed_by(self.user1, self.user))
        self.assertFalse(User.is_followed_by(self.user, self.user1))
        self.assertFalse(User.is_followed_by(self.user, self.user2))

    def test_signup(self):
        """Does test_signup method work?"""


        # is new user an instance of the User class
        self.assertIsInstance(User.signup(username="testuser2", 
                                        email="test2@test.com", 
                                        password="HASHED_PASSWORD1", 
                                        image_url=""), 
                                User)
        self.assertRaises(ValueError, User.signup(username="", 
                                        email="", 
                                        password="", 
                                        image_url=""))


