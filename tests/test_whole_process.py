import unittest

from outputting.ouput_data import output_data
from outputting.process_document import process_document


class TestWholeProcess(unittest.TestCase):
    def test_letters_numbers_boxes_recognized_output_created(self):
        document_path = "tests/form_for_test/document.jpg"
        form_data = process_document("./tests/path_config.json", document_path)
        self.assertEqual((False, False, False, True, False), form_data.fields[0].recognized)
        self.assertEqual(("0", "3", " ", "0", "5", " ", "2", "0", "2", "0"), form_data.fields[1].recognized)
        self.assertEqual(("R", "Y", "C", "H", "L", "Y", " ", "M", "Q", "U", "C", "H", "Y"), form_data.fields[2].recognized)

        self.assertEqual("tests/form_for_test/document.xlsx", output_data(form_data, document_path))
