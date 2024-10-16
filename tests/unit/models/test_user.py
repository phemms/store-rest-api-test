from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest
import unittest

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('user1', 'querty')

        self.assertEqual(user.username, 'user1')
        self.assertEqual(user.password, 'querty')

