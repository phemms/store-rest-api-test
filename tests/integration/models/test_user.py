from models.user import UserModel
from tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('user1', 'qwerty')

            self.assertIsNone(UserModel.find_by_username('user1'), 'no username expected')
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('user1'), 'username expected')
            self.assertIsNotNone(UserModel.find_by_id(1))