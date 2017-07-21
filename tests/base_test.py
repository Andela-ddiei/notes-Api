import unittest
from models import db, User
from faker import Factory
from run import app

fake = Factory.create()


class BaseTest(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfiguration')
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

        self.password = fake.password()

        self.user = User(
            username=fake.user_name(),
            password=User.hash_password(self.password)
        )

        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
