from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')
            store.save_to_db()
            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()
            store.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))


    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            store.save_to_db()

            item = ItemModel('cookies', 1.29, store.id)

            item.save_to_db()

            self.assertEqual(item.store.name, 'test_store')
