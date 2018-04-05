__package__ = "application"

from flask import Flask,g,session
from os import urandom
from config import BaseConfig
import logging.config

app = Flask(__name__,template_folder='templates')

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_current_user():
    from .database import get_db
    user_result = None
    if 'username' in session:
        user = session['username']
        db = get_db()
        user_cur = db.execute('select id,name,password,expert,admin from users where name = ?',[user])
        user_result = user_cur.fetchone()
    return user_result

from views import *

app.config.from_object(BaseConfig)
log_config = app.config['LOGGING_CONFIG']
logging.config.dictConfig(log_config)
logger = logging.getLogger("question_answer_app")
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

