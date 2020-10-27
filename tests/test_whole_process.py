import unittest

import pandas as pd

from outputting.ouput_data import output_data, save_data
from outputting.process_document import process_document


class TestWholeProcess(unittest.TestCase):
    def test_letters_numbers_boxes_recognized_output_created(self):
        document_path = "tests/form_for_test/document.jpg"
        form_data = process_document("./tests/path_config.json", document_path)
        self.assertEqual((False, False, False, True, False), form_data[0].fields[0].recognized)
        self.assertEqual(("0", "3", " ", "0", "5", " ", "2", "0", "2", "0"), form_data[0].fields[1].recognized)
        self.assertEqual(("R", "Y", "C", "H", "L", "Y", " ", "M", "Q", "U", "C", "H", "Y"),
                         form_data[0].fields[2].recognized)
        exp = pd.DataFrame(
            index=[0, 1, 2, 3],
            data={
                "name": ["Spali jste během Unihacku?", "Datum vyplnění", "Jméno týmu", "Chcete přepis, nebo zmrzlinu?"],
                "data": ["Výjimečně.", "03 05 2020", "RYCHLY MQUCHY", "Procházka a zmrzlina!"]
            })

        df, images = output_data(form_data)
        pd.testing.assert_frame_equal(exp, df[["name", "data"]])
        save_data(df, images, document_path)
