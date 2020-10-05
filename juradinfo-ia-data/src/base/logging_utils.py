"""
Module to define usefull logging functions across the project;
"""
import sys
import os

sys.path.append(
    os.path.dirname(__file__)
)  # path of the directory containing the current file : os.path.dirname(__file__)

from pathlib import Path
import logging
from datetime import date

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
)
today = date.today()
LOG_FILE = os.path.join(
    os.path.dirname(__file__), "../../logs/ocr_{}.log".format(today)
)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, name="ocr"):
    today = date.today()
    LOG_FILE = os.path.join(
        os.path.dirname(__file__), "../../logs/{}_{}.log".format(name, today)
    )
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
