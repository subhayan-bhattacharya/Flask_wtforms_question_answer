import sqlite3
from flask import g
import os
import sys
from application import app

def connect_db():
    app.logger.debug("Inside connect_db function")
    db_path = app.config['DB_PATH']
    if os.path.exists(db_path):
        app.logger.info("database path : %s ",db_path)
        sql = sqlite3.connect(db_path)
    else:
        app.logger.error("Could not find db file for loading")
        sys.exit()
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    app.logger.debug("Inside get db function")
    if not hasattr(g, 'sqlite_db'):
        app.logger.debug("Adding sqlite_db to g global variable")
        g.sqlite_db = connect_db()
    return g.sqlite_db