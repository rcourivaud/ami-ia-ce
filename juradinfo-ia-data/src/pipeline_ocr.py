"""
Execute OCR pipeline on files inside the input directory
"""
import time
import sys

import os


sys.path.append(
    os.path.dirname(__file__)
)  # path of the directory containing the current file : os.path.dirname(__file__)

from ocr_concurrent import OcrConcurrent as ocrc
from ocr import Ocr as ocr
from base.env import App
from base.utils import Utils
from base import logging_utils as log

pipeline_logger = log.get_logger(__name__)

input_dir = App.get_input_dir()
filter_criteria = App.get_filter_criteria()
pdf_files = Utils.filter(Utils.get_pdf_files(input_dir), filter_criteria,)
folder_format = App.get_folder_format()

nb_thread = App.get_nb_thread()
os.environ["TIKA_SERVER_JAR"] = App.get_tika_jar()

if __name__ == "__main__":
    import time

    pipeline_logger.info("Starting the pipeline")

    start_time = time.time()

    lst_pdf_text, lst_pdf_scan = ocr.check_if_is_scan(pdf_files)

    print(f"\n\n\nLa liste des fichiers pdf texte : {lst_pdf_text}\n *******************\n")
    print(f"\n\n\nLa liste des fichiers pdf scannée : {lst_pdf_scan} \n ****************\n")



    lst_pdf_text = sorted(lst_pdf_text, key=lambda f: os.stat(f).st_size if f is not None else 0)
    lst_pdf_scan = sorted(lst_pdf_scan, key=lambda f: os.stat(f).st_size if f is not None else 0)

    ocrc.concurrent_ocr(nb_thread, lst_pdf_text, folder_format, True)
    ocrc.concurrent_ocr(nb_thread, lst_pdf_scan, folder_format, False)

    elapsed_time = time.time() - start_time

    pipeline_logger.info("End of the execution of the pipeline")

    pipeline_logger.info(
        f"Number the of threads used : {nb_thread}, number of pdf files to treat : {len(pdf_files)}, duration of the execution : {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}"
    )
