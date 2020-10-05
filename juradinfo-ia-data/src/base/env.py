import os
import sys

sys.path.append(
    os.path.dirname(__file__)
)  # path of the directory containing the current file : os.path.dirname(__file__)

from config_reader import Config


class App:
    """
    class to get information from the configuration file
    """

    def __init__(self):
        pass

    @classmethod
    def get_os(cls):
        """ :returns the Operating System mention in configuration file"""
        return Config.read_config_data("details", "os")

    @classmethod
    def get_os_separator(cls):
        """ :returns the Operating System Separator"""
        sep = ""
        if cls.get_os() == "Linux":
            sep = "/"
        else:
            sep = "\\"
        return sep

    @classmethod
    def get_language(cls):
        """ :returns the language of the files to OCR"""
        return Config.read_config_data("details", "language")

    @classmethod
    def get_nb_thread(cls):
        """ :returns the number of thread to use during concurrent OCR process"""
        return int(Config.read_config_data("details", "nb_thread"))

    @classmethod
    def get_tesseract_path(cls):
        """ :returns the path of tesseract executable"""
        return Config.read_config_data("details", "tesseract_path")

    @classmethod
    def get_db_user(cls):
        """ :returns the username of the database"""
        return Config.read_config_data("database", "user")

    @classmethod
    def get_db_pwd(cls):
        """ :returns the password of the database"""
        return Config.read_config_data("database", "pwd")

    @classmethod
    def get_db_host(cls):
        """ :returns the hostname of the database"""
        return Config.read_config_data("database", "host")

    @classmethod
    def get_db_name(cls):
        """ :returns the database name of the database"""
        return Config.read_config_data("database", "name")

    @classmethod
    def get_db_dialecte(cls):
        """ :returns the dialecte of the database"""
        return Config.read_config_data("database", "dialecte")

    @classmethod
    def get_db_table_name(cls):
        """ :returns the tablename of the database"""
        return Config.read_config_data("database", "table_name")

    @classmethod
    def get_tika_jar(cls):
        """:returns the path or tika-server.jar"""
        return Config.read_config_data("tika", "jar")


    @classmethod
    def get_tika_port(cls):
        """:returns the port used by tika-server"""
        return Config.read_config_data("tika", "port")

    @classmethod
    def get_path_to_tika_sever(cls):
        """:returns the path of tika-server"""
        port = cls.get_tika_port()
        path_to_server = "http://localhost:" + port
        return path_to_server

    @classmethod
    def get_threshold(cls):
        """ :returns the treshold that identify if the pdf is an image pdf"""
        return int(Config.read_config_data("details", "threshold"))

    @classmethod
    def get_spacy_model(cls):
        """ :returns the model to use with spacy"""
        return Config.read_config_data("spacy", "model")

    @classmethod
    def get_input_dir(cls):
        """ :returns the model to use with spacy"""
        return Config.read_config_data("exec", "input_dir")

    @classmethod
    def get_filter_criteria(cls):
        """ :returns the model to use with spacy"""
        return Config.read_config_data("exec", "filter_criteria").split("/")

    @classmethod
    def get_folder_format(cls):
        """ :returns the model to use with spacy"""
        return Config.read_config_data("exec", "folder_format")
