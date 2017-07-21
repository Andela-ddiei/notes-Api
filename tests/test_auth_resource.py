from base_test import BaseTest
from faker import Factory

fake = Factory.create()


class AuthResource(BaseTest):
    def test_login(self):
        user_data = {
            "username": self.user.username,
            "password": self.password
        }
        response = self.client.post('/users/login', data=user_data)
        self.assertTrue("token" in response.data.decode("ascii"))
        self.assertEqual(200, response.status_code)

    def test_login_invalid_password(self):
        user_data = {
            "username": self.user.username,
            "password": "password"
        }
        response = self.client.post('/users/login', data=user_data)
        self.assertTrue("Invalid password" in response.data.decode("ascii"))
        self.assertEqual(403, response.status_code)

