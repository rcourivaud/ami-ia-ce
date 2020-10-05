"""
Module containing the definition of the Ocr class.
"""
import time
import sys
import os

sys.path.append(
    os.path.dirname(__file__)
)  # path of the directory containing the current file : os.path.dirname(__file__)

import re

from PIL import Image
import pytesseract
from pdf2image import pdfinfo_from_path, convert_from_path

import glob
from pathlib import Path

from base import logging_utils as log
from base.env import App
from base.utils import Utils

import spacy

model = App.get_spacy_model()
nlp = spacy.load(model)

from spellchecker import SpellChecker

lg = App.get_language()
spell = SpellChecker(language=lg[0:2])

import logging.config
import shutil

library = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../external_libraries/tika-server.jar")
)

path_to_server = App.get_path_to_tika_sever()
# os.system("chmod +x " + library)
# os.system("java -jar " + library + " --port " + port)

import tika

tika.TikaClientOnly = True
from tika import parser

import multiprocessing as mp

os_ = App.get_os()
sep = App.get_os_separator()
THRESHOLD = App.get_threshold()


if os_ == "Windows":
    pytesseract.pytesseract.tesseract_cmd = App.get_tesseract_path()

ocr_logger = log.get_logger(__name__)

escape_dict = Utils.get_escape_dict()


class Ocr:
    """
	Class to manage OCR actions.
	"""

    @classmethod
    def create_folder(cls, folder):
        """Create a folder if it doesn't exist
           :param folder : the folder name to create
           :returns 0 : if everything goes well
        """
        ocr_logger.info("Calling create_folder(cls, folder)")
        try:
            Path(folder).mkdir(parents=True, exist_ok=True)
            ocr_logger.info("Done with create_folder(cls, folder)")
            return 0
        except:
            ocr_logger.error("create_folder failed", exc_info=True)
            raise Exception("create_folder failed")

    @classmethod
    def nb_jpg_in_folder(cls, folder):
        """:returns n: the number of jpg images in a specify folder
           :param folder : the folder where to count the number of jpg files
        """
        ocr_logger.info("Calling  nb_jpg_in_folder(cls, folder)")
        l = glob.glob(os.path.join(folder, "*.jpg"))
        n = len(l)
        ocr_logger.info("Done with  nb_jpg_in_folder(cls, folder)")
        return n

    @classmethod
    def pdf2images(cls, filename, folder_of_pdf, folder_of_images):
        """Convert a pdf file into set of jpg images, one image for one page of the pdf file
           :param filename : the name of the pdf file to treat
           :param folder_of_pdf : the path to the pdf folder
           :param folder_of_images : the path to the folder where to save images
           :returns 0 : if everythings goes well
        """
        ocr_logger.info(
            "Calling  pdf2images(cls, filename, folder_of_pdf, folder_of_images)"
        )
        cls.create_folder(folder_of_images)

        path_filename = os.path.join(folder_of_pdf, filename)
        jpg_file, _ = filename.split(".")
        idx = 0

        try:
            info = pdfinfo_from_path(
                path_filename, userpw=None, poppler_path="/usr/bin"
            )
            max_pages = info["Pages"]

            lst = list(range(1, max_pages, 10)) if max_pages > 1 else [1]
            for start_idx in lst:
                pages = convert_from_path(
                    path_filename,
                    dpi=500,
                    poppler_path="/usr/bin",
                    fmt="jpeg",
                    first_page=start_idx,
                    last_page=min(start_idx + 10 - 1, max_pages),
                )
                for page in pages:
                    path_jpg_file = os.path.join(
                        folder_of_images, f"{jpg_file}-{idx}.jpg"
                    )
                    page.save(path_jpg_file, "JPEG")
                    idx = idx + 1

            ocr_logger.info(
                "Done with  pdf2images(cls, filename, folder_of_pdf, folder_of_images)"
            )
            return 0
        except:
            ocr_logger.error(
                f"pdf2images failed, file : '{path_filename} ", exc_info=True
            )
            raise Exception(f"pdf2images failed, file : {path_filename}")

    @classmethod
    def preprocess_image(cls, img):
        """Preprocess an image before OCR operation"""
        ocr_logger.info("Calling  preprocess_image(cls, img)")
        pass

    @classmethod
    def split_into_lines(cls, text, sep):
        """"Split a text into lines
        :param text : the text to treat
        :param sep : the separator of lines usually it is \\n
        :returns a list of lines"""
        ocr_logger.info("Calling split_into_lines(text, sep)")
        return text.split(sep)

    @classmethod
    def number_of_lines(cls, text, sep):
        """ Count the number of lines in a text
        :param text : the text to treat
        :param sep : the separator of lines"""
        ocr_logger.info("Calling number of lines")
        lst_sentences = cls.split_into_lines(text, sep)
        return len(lst_sentences)

    @classmethod
    def split_into_chuncks(cls, text, sep):
        """Split a text into chuncks
        :param text: the text to treat
        :param sep : the separator of lines
        :returns : three paragraphs corresponding to head, body and the end of the text"""
        ocr_logger.info("Calling split_into_chuncks")
        lst_sentences = cls.split_into_lines(text, sep)
        n = cls.number_of_lines(text, sep)
        nn = n // 3
        if n < 100:
            text_entete = lst_sentences[0:nn]
            text_corp = lst_sentences[nn : (2 * nn)]
            text_fin = lst_sentences[(2 * nn) :]
        else:
            text_entete = lst_sentences[0:25]
            text_corp = lst_sentences[25 : (n - 35)]
            text_fin = lst_sentences[(n - 35) :]

        ocr_logger.info("Done with split_into_chuncks(text, sep)")
        return text_entete, text_fin, text_corp

    # https://www.coder.work/article/4933069
    @classmethod
    def str_to_raw(cls, s):
        """Convert a normal string into raw string
        :param s: the string to treat
        :returns : the raw string"""
        ocr_logger.info("Calling str_to_raw")
        return r"".join(escape_dict.get(c, c) for c in s)

    @classmethod
    def remove_from_list(cls, lst, to_delete):
        """Remove a word from a list of words
        :param lst : the list of words
        :param to_delete : the word to delete
        :returns: the list of words except the word to delete"""
        ocr_logger.info("Calling remove_from_list")
        return [e for e in lst if e.lower() != to_delete.lower()]

    @classmethod
    def delete_misspelled(cls, txt):
        """ Dilate misspelled word in the beginning and the end of the text
        :param text : the text to treat
        :returns the text without misspleled words"""

        ocr_logger.info("Calling delete_misspelled(txt)")

        try:
            t = txt
            doc = nlp(txt)
            lst_words = [token.text for token in doc]

            misspelled = spell.unknown(lst_words)

            p = re.compile(r"^\d+[-_—]*\d*")
            lst_m = [s for s in misspelled if not p.search(s)]
            if len(lst_m) / (len(lst_words) + 0.001) >= 0.2:
                return ""

            for m in lst_m:
                if m == spell.correction(m):
                    try:
                        lst_words = cls.remove_from_list(lst_words, m)
                    except:
                        lst_words = cls.remove_from_list(lst_words, cls.str_to_raw(m))

            ocr_logger.info("Done with delete_misspelled(txt)")

            return " ".join(lst_words)
        except:
            ocr_logger.info("Done with delete_misspelled(txt)")
            return ""

    @classmethod
    def delete_stamp(cls, text, sep):
        """delete misspelled word corresponding to a stamp in a text
        :param text: the text to treat
        :param sep: the separator of lines
        :returns the text without misspelled word corresponding to stamp"""

        ocr_logger.info("Calling delete_stamp(text, sep)")

        lst_chuncks = cls.split_into_chuncks(text, sep)
        t = []

        for ch in lst_chuncks[0:-1]:
            r = []
            for lgn in ch:
                lgn = cls.delete_misspelled(lgn)
                lgn2 = re.sub(
                    r"[“”'‘’\"@&\!\?«»\-_—;,:\.…\\\$/\*%\€][ ”“'‘’\"@&\!\?«\-_—;,:\.…\\\$/\*%\€]{2,}",
                    "",
                    lgn,
                )
                if 1 - (len(lgn2) / (len(lgn) + 0.001)) > 0.3:
                    lgn2 = ""
                r.append(lgn2)
            t.append(sep.join(r))

        txt = sep.join([t[0], sep.join(lst_chuncks[2]), t[1]])

        ocr_logger.info("Done with delete_stamp(text, sep)")

        return txt

    @classmethod
    def post_process_pdf_image(cls, txt):
        """Postprocess text after the ocr with tesseract-ocr
        :param text: the text to postprocess
        :returns the postproscess text"""
        ocr_logger.info("Calling post_process_pdf_imate(txt)")
        start_time = time.time()

        text = str(txt)
        text = re.sub(r"TA-[a-zA-Z]* [0-9]*.*", "", text)  # Delete timestamp from text
        text = re.sub(r"[\n]{3,}", "\n\n", text)
        text = re.sub(r"[ ]+", " ", text)
        text = cls.delete_stamp(text, "\n")
        text = re.sub(r"(?<=[^\n])\n(?=[^\n])", " ", text)
        text = re.sub(r"[‘’]+", "'", text)
        text = re.sub(r"[\n]{3,}", "\n\n", text)
        text = re.sub(r"^[\n]+", "", text)
        text = text.replace("\n", "###")
        text = re.sub(r"page [0-9]+ sur [0-9]+", "", text, flags=re.IGNORECASE)
        text = re.sub(r" +###", "###", text)
        text = re.sub(r"### +", "###", text)

        elapsed_time = time.time() - start_time
        ocr_logger.info(
            f"Done with post_process_pdf_text(cls, img), duration of the execution: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}"
        )
        return text

    @classmethod
    def post_process_pdf_text(cls, text):
        """Post process text after extraction with apache tika
        :param text : the text to postprocess
        :returns: the postprocess text"""
        ocr_logger.info("Calling post_process_pdf_text(text)")

        txt = re.sub(r"^[\n]+", "", text)
        txt = re.sub(r"\ner\n", "er\n", txt)
        txt = re.sub(r"\nème\n", "ème\n", txt)
        lgns = txt.split("\n")
        ls_lg = []
        for lg in lgns:
            lg_p = re.sub(r"^[-():\w ]{1,3}$", "\n", lg)
            ls_lg.append(lg_p)
        txt = "\n".join(ls_lg)
        txt = re.sub(r"\n{2}", "\n", txt)
        txt = re.sub(r"[\n]{3,}", "\n\n", txt)
        txt = txt.replace("\n", "###")
        txt = re.sub(r"page [0-9]+ sur [0-9]+", "", txt, flags=re.IGNORECASE)
        txt = re.sub(r" +###", "###", txt)
        txt = re.sub(r"### +", "###", txt)

        ocr_logger.info("Done with post_process_pdf_text(text)")

        return txt

    @classmethod
    def ocr_image(cls, img):
        """Extract text from an image
           :param img: the image file to OCR
           :returns t: the text extract from the image
        """
        ocr_logger.info("Calling   ocr_image(cls, img)")
        try:
            t = pytesseract.image_to_string(Image.open(img), lang=lg)
            ocr_logger.info("Done with   ocr_image(cls, img)")
            return t
        except:
            ocr_logger.error(f"ocr_image failed, file : {img}", exc_info=True)
            raise Exception("ocr_image failed")

    @classmethod
    def ocr_pdf_image(cls, folder_of_pdf, filename, prefix="."):
        """
        Extract a text from à pdf of images
        :param folder_of_pdf : the folder that containt the pdf to OCR
        :param filename : the pdf file to OCR
        :param prefix : the folder where to store images
        :returns text, img_folder : the text of the pdf and the folder of images
        """
        ocr_logger.info("Calling  ocr_pdf_image(cls, folder_of_pdf, filename)")
        start_time = time.time()
        result_folder, _ = filename.split(".")
        img_folder = os.path.join(prefix, result_folder)
        cls.pdf2images(filename, folder_of_pdf, img_folder)
        nb_page = cls.nb_jpg_in_folder(img_folder)

        text = ""
        try:
            if nb_page == 1:
                img_filename = glob.glob(os.path.join(img_folder, "*.jpg"))[0]
                text = cls.ocr_image(img_filename)
                ocr_logger.info(
                    "Done with  ocr_pdf_image(cls, folder_of_pdf, filename)"
                )
            else:

                for idx in range(nb_page):
                    img_filename = (
                        os.path.join(img_folder, result_folder)
                        + "-"
                        + str(idx)
                        + ".jpg"
                    )
                    text += "\n"
                    text += cls.ocr_image(img_filename)
            elapsed_time = time.time() - start_time
            ocr_logger.info(
                f"Done with  ocr_pdf_image(cls, folder_of_pdf, filename), duration of the execution : {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}"
            )
            path = os.path.join(folder_of_pdf, filename)
            text = cls.post_process_pdf_image(text)
            return text, img_folder, nb_page, path
        except:
            ocr_logger.error(f"ocr_pdf_image failed, file : {filename}", exc_info=True)
            raise Exception("ocr_pdf_image failed")

    @classmethod
    def ocr_pdf_text(cls, path, post_p=True):
        """Extract text from pdf of text
        :param path : the path to the pdf file
        :returns the text of the pdf file"""
        ocr_logger.info(f"Calling   ocr_pdf_text(cls, {path})")
        start_time = time.time()
        try:
            parsed = parser.from_file(path, path_to_server)
            txt = parsed["content"]
            nb_page = int(parsed["metadata"]["xmpTPg:NPages"])
            elapsed_time = time.time() - start_time
            ocr_logger.info(
                f"Done with ocr_pdf_text(cls, path), duration of the execution : {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}"
            )
            if post_p:
                txt = cls.post_process_pdf_text(txt)
            return txt, None, nb_page, path
        except:
            ocr_logger.error(f"Unable to ocr file : {path}", exc_info=True)
            return None, None, None, None

    @classmethod
    def ocr_request(cls, path, b_tika):
        """
        Transform a request into a set of images, and extract text from those images
        :param path : the path of the request to OCR
        :returns txt : the texte of the request
        """
        ocr_logger.info(f"Calling ocr_request(cls, {path})")
        # extract texte from pdffile
        txt = None
        is_scan = not b_tika
        if b_tika:
            txt, imgfoder, nb_page, file_path = cls.ocr_pdf_text(path)
        else:
            lst = path.split(sep)
            filename = lst[-1]
            folder_pdf = sep.join(lst[0:-1])
            txt, imgfoder, nb_page, file_path = cls.ocr_pdf_image(
                folder_pdf, filename, folder_pdf
            )

        try:
            if imgfoder is not None:
                shutil.rmtree(imgfoder)
            ocr_logger.info("Done with ocr_request(cls, path)")
            return txt, nb_page, file_path, is_scan
        except OSError as e:
            ocr_logger.error("Error: %s - %s." % (e.filename, e.strerror))
            print("Error: %s - %s." % (e.filename, e.strerror))

    @classmethod
    def check_if_is_scan(cls, lst_pdf_files):
        """
        This function split the list of pdf files into pdf texte and pdf scan
        :param lst_pdf_files: list of pdf files
        :return: lst_pdf_text and lst_pdf_scan : the list of pdf texte and the list of pdf scan
        """
        lst_pdf_scan = []
        lst_pdf_text = []

        # Step 1: Init multiprocessing.Pool()
        pool = mp.Pool(mp.cpu_count())

        # Step 2: `pool.apply` the `howmany_within_range()`
        results = [pool.apply(cls.ocr_pdf_text, args=(p, False)) for p in lst_pdf_files]

        # Step 3: Don't forget to close
        pool.close()

        for r in results:
            txt = r[0]
            is_scan = txt is None or (len(txt) / float(r[2])) < THRESHOLD
            if is_scan:
                lst_pdf_scan.append(r[3])
            else:
                lst_pdf_text.append(r[3])

        return lst_pdf_text, lst_pdf_scan
