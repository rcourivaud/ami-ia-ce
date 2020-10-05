"""
Module to define usefull functions across the project;
"""
import sys
import os

sys.path.append(os.path.dirname(__file__))

from config_reader import Config


class Utils:
    def __init__(self):
        pass

    @classmethod
    def get_pdf_files(cls, input_dir):
        """ :returns the list of all pdf files containt in a folder and its subfolders
            :param input_dir: folder that containt pdffiles"""
        lst_files = [
            os.path.join(root, name)
            for root, dirs, files in os.walk(input_dir)
            for name in files
            if name.endswith(".pdf")
        ]

        return lst_files

    @classmethod
    def filter(cls, lst_to_filter, lst_pattern):
        return [
            e for e in lst_to_filter if any(pattern in e for pattern in lst_pattern)
        ]

    @classmethod
    def get_escape_dict(cls):
        escape_dict = {
            "\a": r"\a",
            "\b": r"\b",
            "\c": r"\c",
            "\f": r"\f",
            "\n": r"\n",
            "\r": r"\r",
            "\t": r"\t",
            "\v": r"\v",
            "'": r"\'",
            '"': r"\"",
            "\0": r"\0",
            "\1": r"\1",
            "\2": r"\2",
            "\3": r"\3",
            "\4": r"\4",
            "\5": r"\5",
            "\6": r"\6",
            "\7": r"\7",
            "\8": r"\8",
            "\9": r"\9",
        }

        return escape_dict
