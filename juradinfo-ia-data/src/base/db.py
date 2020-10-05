"""
Contains definition of DataBase class.
"""

import os
import sys

sys.path.append(
    os.path.dirname(__file__)
)  # path of the directory containing the current file : os.path.dirname(__file__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config_reader import Config
from env import App


db_param = {}


class DataBase:
    """
	Manage database actions
	"""

    def __init__(self):
        pass

    @classmethod
    def get_db_uri(cls):
        """ :returns the URI of the database"""
        db_uri = "{dialecte}://{username}:{password}@{hostname}/{databasename}".format(
            dialecte=App.get_db_dialecte(),
            username=App.get_db_user(),
            password=App.get_db_pwd(),
            hostname=App.get_db_host(),
            databasename=App.get_db_name(),
        )

        return db_uri

    @classmethod
    def initialize(cls):
        """:returns the connexion engine and the session of the database"""
        db_param["engine"] = create_engine(cls.get_db_uri())
        Session = sessionmaker(bind=db_param["engine"])
        db_param["session"] = Session()

        return db_param

    @classmethod
    def get_engine(cls):
        try:
            return db_param["engine"]
        except:
            return None
