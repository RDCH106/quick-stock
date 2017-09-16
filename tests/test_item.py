# -*- coding: utf-8 -*-

import unittest
from quickstock import quickStock, common

class TestClass(unittest.TestCase):

    def setUp(self):
        self.qs = quickStock.QuickStock()


    def test_constructor(self):
        self.assertIsInstance(self.qs, quickStock.QuickStock, "Object is not an instance of QuickStock")


class TestClassMethods(unittest.TestCase):

    def setUp(self):
        self.qs = quickStock.QuickStock()
        self.qs.flushStocks()
        self.qs.addStock("My Stock", 123)
        self.qs.flushItems()

    def tearDown(self):
        self.qs.flushall()

    def test_addItem(self):
        numItems = len(self.qs.getStockItems(1))
        self.qs.addItem("Apple", 106, 1)
        self.assertLess(numItems, len(self.qs.getStockItems(1)))

    def test_getItem(self):
        self.qs.addItem("Apple", 106, 1)
        self.assertEqual("Apple", self.qs.getItem(1).name)
        self.assertEqual(106, self.qs.getItem(1).amount)
        self.assertEqual(1, self.qs.getItem(1).stock_id)

    def test_getStockItems(self):
        self.qs.addItem("Apple", 106, 1)
        self.qs.addItem("Orange", 107, 1)
        self.assertEqual(2, len(self.qs.getStockItems(1)))
        self.assertEqual("Apple", self.qs.getItem(1).name)
        self.assertEqual(106, self.qs.getItem(1).amount)
        self.assertEqual(1, self.qs.getItem(1).stock_id)
        self.assertEqual("Apple", self.qs.getItem(1).name)
        self.assertEqual(106, self.qs.getItem(1).amount)
        self.assertEqual(1, self.qs.getItem(1).stock_id)

    def test_updateItem(self):
        self.qs.addItem("Apple", 106, 1)
        self.qs.updateItem(1, "Orange", 601)
        self.assertEqual("Orange", self.qs.getItem(1).name)
        self.assertEqual(601, self.qs.getItem(1).amount)

    def test_deleteItem(self):
        self.qs.addItem("Apple", 106, 1)
        self.qs.deleteItem(1)
        self.assertIsNone(self.qs.getItem(1))

    def test_stringifyItemToList(self):
        self.qs.addItem("Apple", 106, 1)
        self.qs.addItem("Orange", 107, 1)
        self.assertEqual("1  Apple 106\n2  Orange 107\n", common.stringifyItemToList(self.qs.getStockItems(1)))


if __name__ == '__main__':
    unittest.main(verbosity=2)