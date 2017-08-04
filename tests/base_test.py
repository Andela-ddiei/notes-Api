import unittest
import json

from models import db, User
from faker import Factory
from run import app


class BaseTest(unittest.TestCase):
    def setUp(self):
        app.config.from_object("config.TestingConfiguration")
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

        self.fake = Factory.create()

        self.password = self.fake.password()

        self.user = User(
            username=self.fake.user_name(),
            password=User.hash_password(self.password)
        )

        db.session.add(self.user)
        db.session.commit()

    def get_token(self, username, password):
        response = self.client.post("/users/login", data={"username": username,
                                    "password": password})
        response_data = json.loads(response.data.decode("ascii"))
        return response_data["token"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
