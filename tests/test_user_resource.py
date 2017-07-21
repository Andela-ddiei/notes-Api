import json

from base_test import BaseTest
from models import db, User


class UserResource(BaseTest):

    def get_token(self, username, password):
        response = self.client.post("/users/login", data={"username": username,
                                    "password": password})
        response_data = json.loads(response.data.decode("ascii"))
        return response_data["token"]

    def test_signup(self):
        user = {
            "username": "test_user",
            "password": "password"
        }

        response = self.client.post("/users", data=user)
        self.assertEqual(201, response.status_code)
        user_id = User.query.filter_by(username="test_user").first().id
        response_data = json.loads(response.data.decode("ascii"))
        self.assertEqual("test_user", response_data["username"])
        self.assertEqual(user_id, response_data["id"])

    def test_get_all_users(self):
        token = self.get_token(self.user.username, self.password)
        response = self.client.get("/users", headers={"Authorization": token})
        response_data = json.loads(response.data.decode("ascii"))
        all_users = User.query.all()
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(all_users), len(response_data))

    def test_get_all_users_without_token(self):
        response = self.client.get("/users")
        self.assertEqual(401, response.status_code)