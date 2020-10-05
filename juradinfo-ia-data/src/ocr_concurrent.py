"""
Contains definition of OcrConcurrent class.
"""
import time
import os
import sys

sys.path.append(
    os.path.dirname(__file__)
)  # path of the directory containing the current file : os.path.dirname(__file__)

from ocr import Ocr
from threading import Thread, RLock
import queue

from base import logging_utils as log
from entities.page import Page
from base.db import DataBase
from base.env import App

lock = RLock()
lst_tread = []
q = queue.Queue()

sep = App.get_os_separator()

ocrc_logger = log.get_logger(__name__)

database = DataBase.initialize()
session = database["session"]
Page.__table__.create(bind=database["engine"], checkfirst=True)


class OcrConcurrent:
    """
    Class to manage parallel execution of the OCR pipeline
    """

    @classmethod
    def filename_segmentation(cls, like, path):
        """
        Extract informations from the path of the request
        :param like: Indicate if the pdffiles are from SKIPPER folder or from Extraction_pdf_series
        :param path: path of the request to OCR
        :return: request_name, num_folder, te, page_number : the request name, the folder number, the court concerned by the request, the page number
        """
        ocrc_logger.info("Calling filename_segementation(cls, like, path)")

        lst = path.split(sep)
        request_name, _ = lst[-1].split(".")
        page_number = "-1"
        ta = ""

        if like == "S":
            num_folder = lst[-2]
            ta = "T75"
        else:
            aux = request_name.split("_")
            num_folder = aux[1]
            ta = aux[0]

        ocrc_logger.info("Done with filename_segmentation(cls, like, path)")

        return request_name, num_folder, ta, page_number

    @classmethod
    def worker(cls, id_thread, like, b_tika):
        """
        Instructions runs by each thread
        :param id_thread : the thread identifier
        :param like : indicate if the request is from  SKIPPER folder or Extraction pdf serie folder
        """

        ocrc_logger.info("Calling woker(cls, id_thread, like)")

        while True:
            path = q.get()
            if path is None:
                break
            ocrc_logger.info("Starting the ocr")
            try:
                start_time = time.time()
                txt, nb_page, file_path, is_scan = Ocr.ocr_request(path, b_tika)
                elapsed_time = time.time() - start_time

                ocrc_logger.info(
                    f"Threads N° {id_thread}, pdf files to ocr : {str(path)}, duration of the ocr : {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}"
                )

                (request_name, num_folder, ta, page_number) = cls.filename_segmentation(
                    like, path
                )
                page = Page(
                    num_folder=num_folder,
                    ta=ta,
                    request_name=request_name,
                    page_number=nb_page,
                    content=txt,
                    file_path=file_path,
                    is_scan=is_scan,
                )
                with lock:
                    ocrc_logger.info("Thread %s: saving results", str(id_thread))

                    session.add(page)
                    session.commit()

                    ocrc_logger.info("Thread %s: finishing", str(id_thread))
                    q.task_done()

            except:
                ocrc_logger.error(
                    f"Threads N° {id_thread}, unable  to ocr : {str(path)}",
                    exc_info=True,
                )

    @classmethod
    def concurrent_ocr(cls, nb_thread, lst_path, like, b_tika):
        """
        Run several threads, each thread for a pdf file
        :param nb_thread : the number the thread to launch
        :param like : indicate whether the request is in the SKIPPER folder or in the Extraction_pdf_series folder
        """

        ocrc_logger.info("Calling concurrent_ocr(cls, nb_thread, lst_path, like):")

        for i in range(nb_thread):
            t = Thread(target=cls.worker, args=(i, like, b_tika))
            t.start()
            lst_tread.append(t)

        for path in lst_path:
            q.put(path)

        # block until all tasks are done
        q.join()

        # stop workers
        for i in range(nb_thread):
            q.put(None)
        for t in lst_tread:
            t.join()

        ocrc_logger.info("Done with concurrent_ocr(cls, nb_thread, lst_path, like)")
