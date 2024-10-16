from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest

class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('lidl')

        self.assertEqual(store.name, 'lidl', 'Unexpected store name')