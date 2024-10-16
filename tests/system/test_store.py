import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/lidl')

                self.assertEqual(response.status_code, 201)
                self.assertEqual(({'name': 'lidl', 'items': []}), json.loads(response.data))
                self.assertIsNotNone(StoreModel.find_by_name('lidl'))

    def test_duplicate_stores(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/lidl')
                response = client.post('/store/lidl')

                self.assertEqual(response.status_code, 400)
                self.assertEqual({'message': "A store with name 'lidl' already exists."}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/lidl')

                self.assertEqual(response.status_code, 201)

                resp = client.delete('/store/lidl')

                self.assertIsNone(StoreModel.find_by_name('lidl'))
                self.assertDictEqual(json.loads(resp.data), {'message': 'Store deleted'})

    def test_retrieve_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/lidl')
                resp = client.get('/store/lidl')

                self.assertEqual(json.loads(resp.data), {'name': 'lidl', 'items': []})
                #print(json.loads(resp.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/lidl')

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Store not found'})

    def test_stores_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/lidl')
                ItemModel('cookies', 1.25, 1).save_to_db()

                resp = client.get('/store/lidl')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'lidl', 'items': [{'name': 'cookies', 'price': 1.25}]},
                                     json.loads(resp.data))

    def test_list_of_stores(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/lidl')
                ItemModel('cookies', 1.25, 1).save_to_db()
                client.post('/store/kmart')
                ItemModel('soda', 2.24, 2).save_to_db()
                client.post('/store/smart')

                resp = client.get('/stores')

                self.assertEqual(json.loads(resp.data),
                                 {'stores': [store.json() for store in StoreModel.query.all()]})

                #print({'stores': [store.json() for store in StoreModel.query.all()]}, '\n')

    def test_list_of_stores_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/lidl')
                ItemModel('cookies', 1.25, 1).save_to_db()
                client.post('/store/kmart')
                ItemModel('soda', 2.24, 2).save_to_db()
                client.post('/store/smart')
                StoreModel('Rkioski').save_to_db()

                resp = client.get('/stores')

                stores_with_items = [store for store in json.loads(resp.data)['stores'] if store['items']]

                expected = {'stores': [store.json() for store in StoreModel.query.all()]}

                self.assertDictEqual({'stores': stores_with_items},
                                     {'stores': [store for store in expected['stores'] if store['items']]})
                #print({'stores': [store for store in expected['stores'] if store['items']]}, '\n')
