from sqlalchemy import null

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                #client.post('/register', json={'username': 'user1', 'password': 'qwerty'})
                UserModel('user1', 'qwerty').save_to_db()
                #print(UserModel.find_by_username('user1'))
                auth_resp = client.post('/auth', data=json.dumps({'username': 'user1',
                                                                  'password': 'qwerty'}),
                                        headers={'Content-Type': 'application/json'})
                #print(auth_resp.headers)
                auth_token = json.loads(auth_resp.data)['access_token']
                #print(auth_token)

                self.access_token = f'Bearer {auth_token}'
                #print(f"Access Token: {self.access_token}")

    def test_get_item_wout_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/cookies')

                self.assertEqual(resp.status_code, 401)

    def test_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/cookies', headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 404)

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('lidl').save_to_db()
                #ItemModel('cookies', 1.25, 1).save_to_db()
                resp = client.post('/item/cookies', json={'price': 1.25, 'store_id': 1})

                self.assertIsNotNone(ItemModel.find_by_name('cookies'))

                #resp = client.get('/item/cookies', headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'cookies', 'price': 1.25}, json.loads(resp.data))

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('lidl').save_to_db()
                ItemModel('cookies', 1.25, 1).save_to_db()
                resp = client.get('/item/cookies',
                                  headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('lidl').save_to_db()
                ItemModel('cookies', 1.25, 1).save_to_db()

                self.assertIsNotNone(ItemModel.find_by_name('cookies'))

                resp = client.delete('/item/cookies')

                self.assertIsNone(ItemModel.find_by_name('cookies'))
                self.assertEqual({'message': 'Item deleted'}, json.loads(resp.data))

                self.assertEqual(resp.status_code, 200)

    def test_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('lidl').save_to_db()
                ItemModel('cookies', 1.25, 1).save_to_db()

                resp = client.post('/item/cookies')

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'cookies' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('lidl').save_to_db()
                resp = client.put('/item/cookies', json={'price': 1.25, 'store_id': 1})

                self.assertIsNotNone(ItemModel.find_by_name('cookies'))

                # resp = client.get('/item/cookies', headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('cookies').price, 1.25)
                self.assertDictEqual({'name': 'cookies', 'price': 1.25}, json.loads(resp.data))

    def test_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('lidl').save_to_db()
                resp = client.post('/item/cookies', json={'price': None, 'store_id': 1})
                resp2 = client.post('/item/cake', json={'price': None, 'store_id': None})

                self.assertEqual(resp.status_code, 201)
                self.assertEqual(resp2.status_code, 201)

                self.assertDictEqual(json.loads(resp2.data), {'name': 'cake', 'price': None})

                resp = client.put('/item/cookies', json={'price': 1.25, 'store_id': 1})
                resp2 = client.put('/item/cake', json={'price': 5.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'cookies', 'price': 1.25})
                self.assertDictEqual(json.loads(resp2.data), {'name': 'cake', 'price': 5.99})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('lidl').save_to_db()
                ItemModel('cake', 5.25, 1).save_to_db()
                client.post('/item/cookies', json={'price': 1.25, 'store_id': 1})

                resp2 = client.get('/items')

                self.assertIsNotNone(resp2.data)
                self.assertEqual(json.loads(resp2.data), {'items': [x.json() for x in ItemModel.query.all()]})

                #print({'items': [x.json() for x in ItemModel.query.all()]})
