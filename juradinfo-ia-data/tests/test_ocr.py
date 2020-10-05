import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(__file__), "../src")
)  # path of the directory containing the current file : os.path.dirname(__file__)

import unittest
from ocr import Ocr
from base.config_reader import Config


test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../testData/"))
input_dir = os.path.join(test_data_dir, "input")
output_dir = os.path.join(test_data_dir, "output")

IMG = os.path.join(input_dir, "images/Bonjour-0.jpg")
FILE1 = os.path.join(input_dir, "pdf_texte_0.pdf")
FILE2 = os.path.join(input_dir, "pdf_texte_2.pdf")


class TestOcrMethods(unittest.TestCase):
    def test_create_folder(self):
        self.assertEqual(
            0,
            Ocr.create_folder(os.path.join(output_dir, "test_folder_created")),
            "create_folder works",
        )

    def test_pdf2image(self):
        pdf_to_test = os.path.basename(FILE1)
        test_pdf2image = os.path.join(output_dir, "test_pdf2image")
        self.assertEqual(
            0, Ocr.pdf2images(pdf_to_test, input_dir, test_pdf2image), "pdf2image works"
        )

    def test_nb_jpg_in_folder(self):
        folder_test = os.path.join(input_dir, "images")
        self.assertEqual(2, Ocr.nb_jpg_in_folder(folder_test), "nb_jpg_in_folder works")

    def test_ocr_image(self):
        self.assertEqual("Bonjour", Ocr.ocr_image(IMG))

    def test_ocr_pdf(self):
        pdf_to_test_1 = os.path.basename(FILE1)
        pdf_to_test_2 = os.path.basename(FILE2)
        self.assertEqual(
            "Bonjour" in Ocr.ocr_pdf_image(input_dir, pdf_to_test_1, output_dir)[0],
            True,
        )
        self.assertEqual(
            "Bonjour Tout le monde",
            Ocr.ocr_pdf_image(input_dir, pdf_to_test_2, output_dir)[0],
        )

    def test_ocr_pdf_image(self):

        pdf_to_test_1 = os.path.join(input_dir, os.path.basename(FILE1))

        t, _, _, _ = Ocr.ocr_pdf_text(pdf_to_test_1)
        t = t.replace("###", "")
        self.assertEqual("Bonjour" in t, True)

    def test_ocr_pdf_text(self):

        pdf_to_test_1 = os.path.join(input_dir, os.path.basename(FILE1))

        t, _, _, _ = Ocr.ocr_pdf_text(pdf_to_test_1)
        t = t.replace("###", "")
        self.assertEqual("Bonjour" in t, True)

    def test_ocr_pdf_request(self):

        pdf_to_test_1 = os.path.join(input_dir, os.path.basename(FILE1))

        t, _, _, _ = Ocr.ocr_request(pdf_to_test_1)
        t = t.replace("###", "")
        self.assertEqual("Bonjour" in t, True)

    def test_remove_from_list(self):

        lst = ["a", "b", "c", "d"]
        lst2 = Ocr.remove_from_list(lst, "a")
        self.assertEqual(3, len(lst2))

    def test_str_to_raw(self):
        s = Ocr.str_to_raw("\q")
        self.assertEqual("\\q", s)

    def test_number_of_lines(self):
        n = Ocr.number_of_lines("\n\n\n", "\n")
        self.assertEqual(n, 4)


if __name__ == "__main__":
    unittest.main()
