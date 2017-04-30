# -*- coding: utf-8 -*-

import logging

from submodules.SimplePythonTools.common import bcolors
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
import json

class quickStock:

    __name__ = "Quick_Stock"

    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
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