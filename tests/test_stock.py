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

    def test_addStock(self):
        numItems = len(self.qs.getAllStocks())
        self.qs.addStock("My Stock", 123)
        self.assertLess(numItems, len(self.qs.getAllStocks()))

    def test_getStock(self):
        self.qs.addStock("My Stock", 123)
        self.assertEqual("My Stock", self.qs.getStock(1).name)
        self.assertEqual(123, self.qs.getStock(1).chat)

    def test_getChatStocks(self):
        self.qs.addStock("My Stock", 123)
        self.qs.addStock("My Stock 2", 123)
        self.assertEqual(2, len(self.qs.getChatStocks(123)))
        self.assertEqual("My Stock", self.qs.getChatStocks(123)[0].name)
        self.assertEqual(123, self.qs.getChatStocks(123)[0].chat)
        self.assertEqual("My Stock 2", self.qs.getChatStocks(123)[1].name)
        self.assertEqual(123, self.qs.getChatStocks(123)[1].chat)

    def test_updateStock(self):
        self.qs.addStock("My Stock", 123)
        self.qs.updateStock(1, "My Stock 2")
        self.assertEqual("My Stock 2", self.qs.getStock(1).name)

    def test_deleteStock(self):
        self.qs.addStock("My Stock", 123)
        self.qs.deleteStock(1)
        self.assertIsNone(self.qs.getStock(1))

    def test_stringifySotckToList(self):
        self.qs.addStock("My Stock", 123)
        self.qs.addStock("My Stock 2", 123)
        self.assertEqual("1  My Stock\n2  My Stock 2\n", common.stringifySotckToList(self.qs.getChatStocks(123)))

if __name__ == '__main__':
    unittest.main(verbosity=2)