from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_user_registration(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', json={'username': 'user1', 'password': 'qwerty'})
                #print(response.headers)
                #print(response.data)

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('user1'))
                self.assertDictEqual({'message': 'User successfully created'}, json.loads(response.data))

    def test_user_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'user1', 'password': 'qwerty'})
                auth_response = client.post('/auth', json={'username': 'user1', 'password': 'qwerty'})

                #print(auth_response.data)
                #print(auth_response.status_code)

                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_user_duplicate(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'user1', 'password': 'qwerty'})
                response = client.post('/register', json={'username': 'user1', 'password': 'qwerty'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exist'}, json.loads(response.data))
