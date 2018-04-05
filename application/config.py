from os import urandom
import logging
import os

SITE_ROOT = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))

class BaseConfig():
    DEBUG = True
    SECRET_KEY = urandom(24)
    DB_PATH = os.path.join(SITE_ROOT,'application\Question_Answer.db')
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "[%(asctime)s] [Level: %(levelname)s] [Path : %(pathname)s]  :Message: %(message)s\n\r"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "root_file_handler": {
                "class": "logging.handlers.WatchedFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "Flask.log",
                "encoding": "utf8"
            },

            "application_file_handler": {
                "class": "logging.handlers.WatchedFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "application.log",
                "encoding": "utf8"
            }
        },

        "loggers": {
            "question_answer_app": {
                "level": "DEBUG",
                "handlers": ["application_file_handler"],
                "propagate": "no"
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["root_file_handler"]
        }
    }