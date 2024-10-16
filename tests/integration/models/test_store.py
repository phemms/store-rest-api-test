from models.item import ItemModel
from models.store import StoreModel

from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        store = StoreModel('Kmart')

        self.assertListEqual(store.items.all(), [], 'store is expected to be empty but it is not')


    def test_crud(self):
        with self.app_context():
            store = StoreModel('lidl')

            self.assertIsNone(StoreModel.find_by_name('lidl'), 'Found a store with name lidl though it was'
                                                               'expected not to exist')

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('lidl'), "Didn't find the store named lidl "
                                                                  "though it should exist; save_to_db() failed")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('lidl'), 'Found store; delete_from_db() did not work')


    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('lidl')
            item = ItemModel('cookies', 1.25, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'cookies')


    def test_store_json(self):
        store = StoreModel('lidl')
        store_type = type(store.json())

        self.assertIsInstance(store_type, type(dict), 'data structures are unequal')
        self.assertEqual(store.json(), {'name': 'lidl', 'items': []})

    def test_store_with_item_json(self):
        with self.app_context():
            store = StoreModel('Kmart')
            item = ItemModel('soda', 2.24, 1)

            store.save_to_db()
            item.save_to_db()

            store_type = type(store.json())
            expected_result = {'name': 'Kmart', 'items': [{'name': 'soda', 'price': 2.24}]}

            self.assertIsInstance(store_type, type(dict), 'data structures are unequal')
            self.assertEqual(store.json(), expected_result)
