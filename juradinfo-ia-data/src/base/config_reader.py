import sys
import os

sys.path.append(
    os.path.dirname(__file__)
)  # path of the directory containing the current file : os.path.dirname(__file__)

import configparser


class Config:
    """
	Class to manage the configuration file.
	"""

    def __init__(self):
        pass

    conf_file_path = os.path.join(os.path.dirname(__file__), "../../config/config.cfg")

    @classmethod
    def read_config_data(cls, section, key):
        """:returns a data containt in the configuration file
           :param section : the section in the configuration file
           :param key the key identifying the element in the section"""
        config = configparser.ConfigParser()
        config.read(cls.conf_file_path)

        return config.get(section, key)
