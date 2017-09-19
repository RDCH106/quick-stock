# -*- coding: utf-8 -*-

import logging

from common import bcolors
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
import json

class QuickStock:

    __name__ = "Quick_Stock"

    logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def loadConfig(logger):
        print(bcolors.WARNING)

        if logger.getEffectiveLevel() != logging.DEBUG:
            logger.info("Running in Release Mode")
        else:
            logger.info("Running in Debug Mode")

        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/../config/config.json') as config_file:
                config = json.load(config_file)
                logger.info("Loaded: config/config.json")
        except IOError:
            print("Error loading config.json!")
            exit()

        print(bcolors.ENDC)
        return (config)

    config = loadConfig(logger)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = config["app"]["secretKey"]
    app.config['SQLALCHEMY_DATABASE_URI'] = config["app"]["databaseUri"]
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = config["app"]["commitOnTeardown"]
    s_db_path = app.config['SQLALCHEMY_DATABASE_URI'].split('//')
    file_path = os.path.dirname(os.path.realpath(__file__))
    databaseUri = s_db_path[0] + "///" + file_path + s_db_path[1]
    app.config['SQLALCHEMY_DATABASE_URI'] = databaseUri
    del (s_db_path, file_path, databaseUri)
    db = SQLAlchemy(app)

    def __init__(self, debug=None):
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.createDB()

    def createDB(self):
        db_path = str(self.app.config['SQLALCHEMY_DATABASE_URI'].split('///')[1])
        if not os.path.exists(db_path):
            print(bcolors.WARNING + "Creating SQlite Database" + bcolors.ENDC)
            print(bcolors.OKBLUE + db_path + bcolors.ENDC)
            self.db.create_all()

    def addStock(self, name, chat):
        stock = Stock(name, chat)
        self.db.session.add(stock)
        self.db.session.commit()
        self.logger.debug("ADD " + repr(stock))

    def getStock(self, id_stock):
        stock = Stock.query.filter_by(id=id_stock).first()
        return stock

    def getAllStocks(self):
        stocks = Stock.query.all()
        return stocks

    def getChatStocks(self, chat):
        stocks = Stock.query.filter_by(chat=chat).all()
        return stocks

    def updateStock(self, id_stock, name):
        stock = Stock.query.get(id_stock)
        stock.name = name
        self.db.session.commit()
        self.logger.debug("UPDATE " + repr(stock))

    def deleteStock(self, id_stock):
        stock = Stock.query.get(id_stock)
        self.db.session.delete(stock)
        self.db.session.commit()
        self.logger.debug("DELETE " + repr(stock))

    def addItem(self, name, amount=None, id_stock=None):
        stock = Stock.query.get(id_stock)
        item = Item(name=name, amount=amount, stock_id=stock.id)
        self.db.session.add(item)
        self.db.session.commit()
        self.logger.debug("ADD " + repr(item))

    def getItem(self, id_item):
        item = Item.query.filter_by(id=id_item).first()
        return item

    def getStockItems(self, stock_id):
        items = Item.query.filter_by(stock_id=stock_id).order_by(Item.name.asc()).all()
        return items

    def updateItem(self, id_item, name=None, amount=None):
        item = Item.query.get(id_item)
        if name is not None:
            item.name = name
        if amount is not None:
            item.amount = amount
        self.db.session.commit()
        self.logger.debug("UPDATE " + repr(item))

    def deleteItem(self, id_item):
        item = Item.query.get(id_item)
        self.db.session.delete(item)
        self.db.session.commit()
        self.logger.debug("DELETE " + repr(item))

    def flushall(self):
        Stock.query.delete()
        Item.query.delete()
        self.db.session.commit()

    def flushStocks(self):
        Stock.query.delete()
        self.db.session.commit()

    def flushItems(self):
        Item.query.delete()
        self.db.session.commit()

class Stock(QuickStock.db.Model):
    __tablename__ = "stock"
    id = QuickStock.db.Column(QuickStock.db.Integer, primary_key=True)
    name = QuickStock.db.Column(QuickStock.db.String(120))
    chat = QuickStock.db.Column(QuickStock.db.Integer)

    def __init__(self, name, chat):
        self.name = name
        self.chat = chat

    def __repr__(self):
        return '<Stock %r - %r ref: %r>' % (self.id, self.name, self.chat)

class Item(QuickStock.db.Model):
    __tablename__ = "item"
    id = QuickStock.db.Column(QuickStock.db.Integer, primary_key=True)
    name = QuickStock.db.Column(QuickStock.db.String(120))
    amount = QuickStock.db.Column(QuickStock.db.Integer)
    stock_id = QuickStock.db.Column(QuickStock.db.Integer)

    def __init__(self, name, amount, stock_id):
        self.name = name
        self.amount = amount
        self.stock_id = stock_id

    def __repr__(self):
        return '<Item %r - %r - %r>' % (self.id, self.name, self.amount)
