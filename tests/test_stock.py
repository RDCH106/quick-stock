# -*- coding: utf-8 -*-

import unittest
from quickstock import quickStock

class TestClass(unittest.TestCase):

    def setUp(self):
        self.qs = quickStock.QuickStock()


    def test_constructor(self):
        self.assertIsInstance(self.qs, quickStock.QuickStock, "Object is not an instance of QuickStock")


class TestClassMethods(unittest.TestCase):

    def setUp(self):
        self.qs = quickStock.QuickStock()
        self.qs.flushStocks()

    def test_addStock(self):
        numItems = len(self.qs.getAllStocks())
        self.qs.addStock("My Stock")
        self.assertLess(numItems, len(self.qs.getAllStocks()))

    def test_getStock(self):
        self.qs.addStock("My Stock")
        self.assertEqual("My Stock", self.qs.getStock(1).name)

    def test_updateStock(self):
        self.qs.addStock("My Stock")
        self.qs.updateStock(1, "My Stock 2")
        self.assertEqual("My Stock 2", self.qs.getStock(1).name)

    def test_deleteStock(self):
        self.qs.addStock("My Stock")
        self.qs.deleteStock(1)
        self.assertIsNone(self.qs.getStock(1))

if __name__ == '__main__':
    unittest.main(verbosity=2)